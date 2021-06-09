import requests
import re
import json
from bs4 import BeautifulSoup
from urllib import parse

class dhlotto:
    __get_recent_round_exp = re.compile(r'<option value="(\d+)" selected>\d+</option>')
    __get_lotto_prize_exp = re.compile(r'')

    __get_lotto_number_cache = dict() # 한번 load한 로또번호는 저장 ( ...[915] = [5, 12, 15, 23, 24, 36, 40] # 915회차 [0]~[5]: 당첨번호, [6]: 보너스)
    __get_lotto_prize_cache = dict() # 한번 load한 당첨금 정보를 저장 ( ...[915] = [55555, 4444, 333, 22, 1] # 915회차 1등상금 55555원, 5등 상금 1원

    def get_recent_round():
        try:
            response = requests.get('https://www.dhlottery.co.kr/gameResult.do?method=byWin')
            return eval(dhlotto.__get_recent_round_exp.findall(response.text)[0])
        except Exception as e:
            print(e)
            return None

    def get_lotto_result(round) -> list():
        try:
            response = requests.get('https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=' + str(round))
            data = json.loads(response.text)
            numbers = []
            for i in range(6):
                numbers.append(data['drwtNo' + str(i+1)])
            numbers.append(data['bnusNo'])
            return {'numbers': numbers, 'date': data['drwNoDate'], 'round': data['drwNo']}
        except Exception as e:
            print(e)
            return None

    def get_lotto_prize(round) -> list():
        try:
            data = {'drwNo': round, 'dwrNoList': round}
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            response = requests.post('https://www.dhlottery.co.kr/gameResult.do?method=byWin', data=data, headers=headers)
            bs = BeautifulSoup(response.text, 'html.parser')
            table_texts = list(map(lambda x : x.text, bs.select('.tbl_data td')))
            del table_texts[5] # 비고 제거
            ret = [[table_texts[x + i * 5] for x in range(4)] for i in range(5)] # 1차원배열 -> 2차원배열 (+ 당첨기준 제거)
            return ret
        except Exception as e:
            print(e)
            return None


    def get_store(city1, city2):
        data = {'searchType':'1', 'nowPage':'1', 'sltSIDO': parse.quote(city1), 'sltGUGUN': parse.quote(city2)}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post('https://www.dhlottery.co.kr/store.do?method=sellerInfo645Result', data=data, headers=headers)
        res_data = json.loads(response.text)

        total_page = res_data['totalPage']

        ret = []
        for x in res_data['arr']:
            ret.append({'name': str(x['FIRMNM']).replace('&&#35;40;', '(').replace('&&#35;41;', ')'), 'lon': x['LONGITUDE'], 'lat': x['LATITUDE'], 'tel': x['RTLRSTRTELNO']})
        for i in range(2, total_page+1):
            data['nowPage'] = i
            response = requests.post('https://www.dhlottery.co.kr/store.do?method=sellerInfo645Result', data=data, headers=headers)
            res_data = json.loads(response.text)
            for x in res_data['arr']:
                ret.append({'name': str(x['FIRMNM']).replace('&&#35;40;', '(').replace('&&#35;41;', ')'), 'lon': x['LONGITUDE'], 'lat': x['LATITUDE'], 'tel': x['RTLRSTRTELNO']})
        return ret

    def get_frequency():
        response = requests.get('https://www.dhlottery.co.kr/gameResult.do?method=statByNumber')
        bs = BeautifulSoup(response.text, 'html.parser')
        tbody = bs.select('#printTarget > tbody')[0]
        tnums = tbody.select('td:nth-of-type(3)')

        return [eval(x.text) for x in tnums]

if __name__ == '__main__':
    dhlotto.get_frequency()