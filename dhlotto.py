import requests
import re
import json

class dhlotto:
    __get_recent_round_exp = re.compile(r'<option value="(\d+)" selected>\d+</option>')

    def get_recent_round():
        try:
            response = requests.get('https://www.dhlottery.co.kr/gameResult.do?method=byWin')
            return eval(dhlotto.__get_recent_round_exp.findall(response.text)[0])
        except:
            return None

    def get_lotto_numbers(round) -> list():
        try:
            response = requests.get('https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=' + str(round))
            print(response.text)
            data = json.load(response.text)
            print(data)
        except:
            return None

if __name__ == '__main__':
    print(dhlotto.get_lotto_numbers(1))