# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
import sched
import time
import main
import time

token = '285455287:AAERVWhSH53FLL1zWERx_u7f7pJJMMP97qA'
method = 'getUpdates'
s = sched.scheduler(time.time, time.sleep)
print('started')
getpost = requests.get(
                url='https://api.telegram.org/bot{0}/{1}'.format(
                    token, method),
                # data={'allowed_updates': ['message'] }
).json()
for mes in getpost['result']:
    print(mes)
    print('---------------')
id_start = getpost['result'][-1]['message']['message_id']
print('start', id_start)


def to_dict(string):
    dictt = {}
    text_array = string.replace("'", "\"").replace(
            "{", "").replace("}", "").replace('"', "").replace(' ', "").split(',')
    for a in text_array:
        b = a.split(':')
        dictt[b[0]] = b[1]
    return dictt


def compute(input_data):
    try:
        a = main.compute(input_data)
        a.start()
    except Exception as e:
        print('ERROR IN COMPUTE')
        print(e)


def do_something(sc):
    global id_start
    try:
        getpost = requests.get(
                        url='https://api.telegram.org/bot{0}/{1}'.format(
                                token, method),
                        # data={'allowed_updates': ['message'] }
        ).json()
    except Exception as e:
        print('ERROR IN GET FROM TELEGRAMM API')
        print(e)
        time.sleep(15)

    try:
        print('состояние нормальное: ', time.asctime(
                time.localtime(time.time())), 'id_mess: ', id_start)
        for mes in getpost['result']:
            current_id = mes['message']['message_id']
            if current_id > id_start:
                res = str(mes['message']['text'])
                print('id to compute: ', id_start)
                compute(to_dict(res))
                id_start = current_id
        # json_acceptable_string = res.replace("'", "\"") # для преобразования в словарь
        # d = json.loads(json_acceptable_string)# для преобразования в словарь

    except Exception as e:
        print('ERROR IN INPUT DATA')
        print(e)
        id_start += 1

    s.enter(60, 1, do_something, (sc,))


s.enter(2, 1, do_something, (s,))
s.run()


# method = 'sendMessage'
# response = requests.post(
#	  url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
#	  data={'chat_id': 180380877, 'text': 'Првиет'}
# ).json()
# print(response)

# print('---------------------------------')
