import requests
import time

a = time.time()
for i in range(10):
    r = requests.get('https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=903')
b = time.time() - a

print('10회에 {0}ms 걸림'.format(int(b * 1000)))
print(r.text)
