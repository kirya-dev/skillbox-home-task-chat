import time
from datetime import datetime

import requests
import threading


DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S'


r = requests.get('http://127.0.0.1:5000/status')
print(r.text)


print('Введите имя пользователя: ', end='')
user = input()
password = None

print('Введите пароль: ', end='')
while True:
    password = input()
    r = requests.post('http://127.0.0.1:5000/auth', json={'user': user, 'password': password})
    if r.json()['ok'] is True:
        break
    print("Пароль неверный. Попробуйие еще: ", end='')


creds = {'user': user, 'password': password}


def listen_new_messages():
    last_time = 0

    while True:
        r = requests.get('http://127.0.0.1:5000/messages', params={'after': last_time})
        messages = r.json().get('messages')
        for mes in messages:
            time_o = datetime.fromtimestamp(mes['time'])
            print(mes['user'] + ('(Вы)' if mes['user'] == user else ''), 'в', time_o.strftime(DATETIME_FORMAT),
                  'говорит:')
            print(mes['text'], '\n')

            last_time = mes['time']

        time.sleep(1)


print("Логин успешно пройден!")


listen = threading.Thread(target=listen_new_messages)
listen.start()


print('------- Диалог --------')


while True:
    text = input()

    print('\033[A', end='')  # move cursor up
    print('                                           ', end='\r')  # clear

    data = creds.copy()
    data['text'] = text
    r = requests.post('http://127.0.0.1:5000/send', json=data)
    if r.json()['ok'] is False:
        print('Ошибка отправки.')
        exit(-1)
