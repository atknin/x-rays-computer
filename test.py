# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import diffraction
import email_module
data = {}
data['pk'] = 808
data['type'] = 0
data['status'] = 'ok'
ff = open('text_json_data','r').read()
data['JSON'] = ff



class_compute = diffraction.compute(data)
print(1000*'*','\n\n',class_compute.show_parametrs(),100*'-')
# расчитать алгоритм
try:
	status = class_compute.start_algoritm()
	title = 'успешно: ' + class_compute.return_input_data()['id_comment_calc']
	text = class_compute.show_parametrs()
except Exception as e:
	title = 'ошибка: ' + class_compute.return_input_data()['id_comment_calc']
	text = ''
	print('неизвестная ошибка')

# отпрвить результаты на почту
email = class_compute.return_input_data()['id_email']
email_module.sendEmail(class_compute.return_path(),email,title,text)
