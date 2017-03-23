# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# import requests
from urllib import request
import urllib.parse as parse
import sched, time
import json
import ast
import main
import time
from computer import *
url = 'http://x-rays.world/diffraction/compute/'
s = sched.scheduler(time.time, time.sleep)
print('started')
son_obj = {}

def to_dict(string):
	dictt = {}
	text_array = string.replace("'", "\"").replace("{", "").replace("}", "").replace('"', "").replace(' ', "").split(',')
	for a in text_array:
		b = a.split(':')
		dictt[b[0]] = b[1]
	return dictt
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
			a = main.compute(to_dict(son_obj['JSON']))
			a.start()
			# все хорошо, сообщаем
			payload = {'complited': son_obj['pk']}
			payload['pc'] = comp
			data = parse.urlencode(payload)
			f = request.urlopen(url + "?" + data)
			print(f.read())
	except Exception as e:
		# ошибка, сообщаем -------сюда не заходит
		payload = {'error_during_compute': son_obj['pk'],'text_error':'ERROR IN do_something: '+ str(e)}
		payload['pc'] = comp
		data = parse.urlencode(payload)
		f = request.urlopen(url + "?" + data)
		print(f.read())
		print(e)
	s.enter(60, 1, do_something, (sc,))
s.enter(2, 1, do_something, (s,))
s.run()
