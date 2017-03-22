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
		payload = {'complited': son_obj['pk']}
		payload['pc'] = comp
		data = parse.urlencode(payload)
		f = request.urlopen(url + "?" + data)
		print(f.read())

	except Exception as e:
		payload = {'error_during_compute': son_obj['pk'],'text_error': str(e)}
		payload['pc'] = comp
		f = request.urlopen(url + "?" + data)
		print(f.read())
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

	except Exception as e:
		print('ERROR IN GET')
		print(e)
		time.sleep(15)


	s.enter(60, 1, do_something, (sc,))

s.enter(2, 1, do_something, (s,))
s.run()
