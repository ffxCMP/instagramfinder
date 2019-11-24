import time
import threading
from image_match.goldberg import ImageSignature
import requests
token = '635777694:AAHbmfWqecHTjz5R1--ZMOT3rRwuNexQknk'

s=0
e=200
f = open('urls.txt')
lines =f.readlines()
num_lines = sum(1 for line in open('urls.txt'))
print(f'загружено фотографий: {num_lines}')
settings = open('find.txt').read().split("\n")
url = settings[0]
print(f'Будем искать: {url}')
gis = ImageSignature()
a = gis.generate_signature(url)

def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}'
    a = requests.post(url)

def th_f(start,end):
    for i in range(start,end):
        try:
            b = gis.generate_signature(lines[i].strip())
            raznica = gis.normalized_distance(a, b)
            if raznica < 0.4:
                print('Нашел похожу картинку. Остылаю в телеграм, проверьте почту!:)')
                chat_id = str(221730817)
                message = lines[i].strip()
                params = {'json': 'true',
                          'url': message}
                data = requests.get(f'https://clck.ru/--?', params=params)
                short_url = data.json()[0]
                send_message(chat_id,f'Нашел INSTAGRAM: {short_url}')
        except Exception as E:
            print(E)
            continue

if __name__ == "__main__":
    threads = list()
    for index in range(num_lines // 200):
        threading.Thread(target=th_f, args=(s, e)).start()
        s += 200
        e += 200
    s = num_lines //200 * 200
    threading.Thread(target=th_f,args=(s,num_lines)).start()