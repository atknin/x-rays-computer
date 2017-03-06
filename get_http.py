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

comp = '1'
url = 'http://x-rays.world/diffraction/compute/'
s = sched.scheduler(time.time, time.sleep)
print('started')

def to_dict(string):
	dictt = {}
	text_array = string.replace("'", "\"").replace("{", "").replace("}", "").replace('"', "").replace(' ', "").split(',')
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
	global url
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
			payload = {'complited': son_obj['pk']}
			payload['pc'] = comp
			data = parse.urlencode(payload)
			f = request.urlopen(url + "?" + data)
			print(f.read())

	except Exception as e:
		print('ERROR IN GET')
		print(e)
		time.sleep(15)

	
	s.enter(60, 1, do_something, (sc,))

s.enter(2, 1, do_something, (s,))
s.run()



# method = 'sendMessage'
# response = requests.post(
#     url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
#     data={'chat_id': 180380877, 'text': 'Првиет'}
# ).json()
# print(response)

# print('---------------------------------')
	

