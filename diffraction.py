# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from output import file_parametres
import os
import zero_crystal
import single_crystal

import double_crystal
import double_crystal_light
from DoubleCrClass import double

import triple_crystal
import triple_crystal_light

from functions import *
import email_module

class compute():
	"""docstring for compute"""
	def __init__(self, input_data):
		print(input_data)
		self.input_data = self.to_dict(input_data['JSON'])
		self.input_data['name_result'] = input_data['pk']        
		self.input_data['path'] = input_data['pk']        
		self.status = 'ok'
		# папка для результатов - путь
		self.path = os.path.dirname(os.path.abspath(__file__))+'/results/'+str(input_data['pk'])
		self.input_data['path'] = self.path
		# создаем папку
		if not os.path.exists(self.path):
			os.makedirs(self.path)
		# добавляем файл параметров
		file_parametres(self.path,self.to_dict(input_data['JSON']))

	def to_dict(self,input_data):

		dictt = {}
		text_array = input_data.replace("'", "\"").replace(
				"{", "").replace("}", "").replace('"', "").replace(' ', "").split(',')
		for a in text_array:
			b = a.split(':')
			dictt[b[0]] = b[1]
		return dictt

	def return_status(self):
		return self.status
	def return_path(self):
		return self.path
	def return_input_data(self):
		return self.input_data

	def start_algoritm(self):
		try:
			if self.input_data['schem'] == 'zero_crystal':
				# self.status = zero_crystal.do_it(self.input_data)
				print('Ноль-кристальный алгоритм отсутсвует')
				return 200
			elif self.input_data['schem'] == 'single_crystal':
				# self.status = single_crystal.do_it(self.input_data)
				print('Одно-кристальный алгоритм отсутсвует')
				return 200
			elif self.input_data['schem'] == 'double_crystal':
				a = double(self.input_data)
				a.start()
				self.status = 200
				return 200
			elif self.input_data['schem'] == 'double_crystal_light':
				a = double(self.input_data)
				a.start()
				self.status = 200
				# self.status = double_crystal_light.do_it(self.input_data)
				# print(self.status)
				return self.status
			elif self.input_data['schem'] == 'triple_crystal':
				# self.status = triple_crystal.do_it(self.input_data)
				print('Трех-кристальный алгоритм отсутсвует')
				return 200
			elif self.input_data['schem'] == 'triple_crystal_light':
				print('Трех-кристальный алгоритм отсутсвует')
				# self.status = triple_crystal_light.do_it(self.input_data)
				return 200
			else:
				return 404
		except Exception as e:
			print(e)
			return 500
	def show_parametrs(self,type = 'text'):
		if type=='text':
			return str(open(self.path+'/info.dat','r').read())
		else:
			return self.input_data



		