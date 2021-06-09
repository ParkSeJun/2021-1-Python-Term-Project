import sys
import telepot
import traceback
from pprint import pprint
import time
import requests
from bs4 import BeautifulSoup


TOKEN = '1892597592:AAGD-VUiqCC8CxD5mIfJSkkXrV0X3zCXglk'
bot = telepot.Bot(TOKEN)
chat_id = 1574057894
baseURL = 'https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo='

#data = requests.get(baseURL +)
#soup = BeautifulSoup(data.text, 'html.parser')
#numberData = soup.find('meta', id='desc')['content']
#print(numberData)


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('회차') and len(args)>1:
        print('try to 회차', args[1])

    else:
        sendMessage(chat_id, '모르는 명령어입니다.\n지역 [지역번호], 저장 [지역번호], 확인 중 하나의 명령을 입력하세요.')


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