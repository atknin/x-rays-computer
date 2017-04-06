# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# import requests
from urllib import request
import urllib.parse as parse
import sched
import time
import json
import main
import time
from computer import *
url = 'http://x-rays.world/diffraction/compute/'
s = sched.scheduler(time.time, time.sleep)
print('started')
son_obj = {}


def to_dict(string):
    dictt = {}
    text_array = string.replace("'", "\"").replace(
            "{", "").replace("}", "").replace('"', "").replace(' ', "").split(',')
    for a in text_array:
        b = a.split(':')
        dictt[b[0]] = b[1]
    return dictt


def compute(inputs):
    global son_obj
    try:
        a = main.compute(inputs)
        a.start()
        # все хорошо, сообщаем
        finish = True
        payload = {'complited': son_obj['pk']}
        payload['pc'] = comp
        data = parse.urlencode(payload)
        while finish:
            f = request.urlopen(url + "?" + data)
            if f.status == 200:
                finish = False
                print('Сообщили об окончании расчета')
            else:
                time.sleep(60)

    except Exception as e:
        # ошибка, сообщаем -------сюда не заходит
        payload = {
                'error_during_compute': son_obj['pk'], 'text_error': 'ERROR IN compute: ' + str(e)}
        payload['pc'] = comp
        data = parse.urlencode(payload)
        f = request.urlopen(url + "?" + data)
        print(f.read())
        print(e)


def do_something(sc):
    global url
    global son_obj
    try:
        payload = {'check': comp}
        data = parse.urlencode(payload)
        f = request.urlopen(url + "?" + data)
        string = f.read().decode('utf-8')
        son_obj = json.loads(string)
        if son_obj['status'] == 'Nodata':
            print('NODATA')
        else:
            compute(to_dict(son_obj['JSON']))
    except Exception as e:
        print('Ошибка в do_something')

    s.enter(60, 1, do_something, (sc,))


s.enter(2, 1, do_something, (s,))
s.run()
