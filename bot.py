import sys
import telepot
import traceback
from pprint import pprint
import time
import requests
from bs4 import BeautifulSoup
import random
import string


TOKEN = '1892597592:AAGD-VUiqCC8CxD5mIfJSkkXrV0X3zCXglk'
bot = telepot.Bot(TOKEN)
chat_id = 1574057894
baseURL = 'https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo='

global data, soup, numberData


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('회차') and len(args)>1:
        print('try to 회차', args[1])
        data = requests.get(baseURL + args[1])
        soup = BeautifulSoup(data.text, 'html.parser')
        numberData = soup.find('meta', id='desc')['content']
        result = numberData.replace(" 당첨번호 ", "\n")
        result = result.replace("+", "\n2등 보너스: ")
        result = result.replace(". ", ".\n")
        result = result.replace(", 1인당 당첨금액 ", ", 각 ")

        if ',,,,,' in result:
            result = str(args[1]) + '회차는 아직 확인되지 않았습니다.'
            return False, sendMessage(chat_id, result)
        if '0,0,0,0,0,0' in result:
            return False, sendMessage(chat_id, '숫자로만 입력해주세요')

        sendMessage(chat_id, result)
        print(numberData)
    elif text.startswith('복권생성') and len(args)>1:
        num = str(args[1])
        if(num.isdigit() == False):
            return False, sendMessage(chat_id, '숫자로만 입력해주세요')

        res = '\n'
        if int(args[1]) > 5:
            return False, sendMessage(chat_id, '복권번호는 최대 5개까지 생성 가능합니다')

        for i in range(0, int(args[1])):
            lotto = random.sample(range(1, 46), 6)
            lotto.sort()
            res += str(lotto) + '\n'
            print(res)

        res2 = '복권 번호를 생성합니다\n' + res + '\n'+str(args[1]) + '개 생성 완료!'
        print(res)
        sendMessage(chat_id, res2)

    elif text.startswith('명령어'):
        sendMessage(chat_id, '회차 [회차번호]\n복권생성 [개수(최대 5)]')

    else:
        sendMessage(chat_id, '모르는 명령어입니다.\n회차 [회차번호], 번호생성 [개수(최대 5)] 중 하나의 명령을 입력하세요.')


def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)




bot = telepot.Bot(TOKEN)
pprint( bot.getMe() )

bot.message_loop(handle)

print('Listening...')

while 1:
  time.sleep(10)