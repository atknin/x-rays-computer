# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import diffraction
import email_module
import os,requests
import matplotlib.pyplot as plt
from functions import *

# data = {}
# data['pk'] = 808
# data['type'] = 0
# data['status'] = 'ok'
# ff = open('text_json_data','r').read()
# data['JSON'] = ff



# class_compute = diffraction.compute(data)
# print(1000*'*','\n\n',class_compute.show_parametrs(),100*'-')
# # расчитать алгоритм
# try:
# 	status = class_compute.start_algoritm()
# 	title = 'успешно: ' + class_compute.return_input_data()['id_comment_calc']
# 	text = class_compute.show_parametrs()
# except Exception as e:
# 	title = 'ошибка: ' + class_compute.return_input_data()['id_comment_calc']
# 	text = ''
# 	print('неизвестная ошибка')

# # отпрвить результаты на почту
# email = class_compute.return_input_data()['id_email']
# email_module.sendEmail(class_compute.return_path(),email,title,text)

# def load_files_to_db(url,path,pk):
#     included_extenstions = ['dat','gif','pdf','docx']
#     file_names = [fn for fn in os.listdir(path+'/')
#                     if any(fn.endswith(ext) for ext in included_extenstions)]
#     print('найдено файлов: ',len(file_names))   
#     files = {}

#     for i in file_names:
#         f = path+'/' + str(i)
#         files[i] = open(f, 'rb')
#     print(files)
#     values = {'pk':pk}
#     r = requests.post(url, files=files, data = values)
#     print('файлы отправлены')
#     return r

# path = '/Users/Atknini/Desktop/open_and_closed'
# url = 'http://62.109.0.242/diffraction/load_files/'
# with open('text.html','w') as a:
# 	v = load_files_to_db(url,path,825).text
# 	a.write(v)
# print(v)
teta = -20
L1 = 0.54
L2 = 0.99
S1 = 0.02/1000
S2 = 0.06/1000
sigma = 0.02/1000
sdvigka = 0
x = []
y = []
while teta<20:
    print(teta,slit_extensive_source(teta,sdvigka,L1,L2,S1,S2,sigma))
    x.append(teta)
    y.append(slit_extensive_source(teta,sdvigka,L1,L2,S1,S2,sigma))
    teta+=1

plt.plot(x,y)
plt.show()




