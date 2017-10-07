# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import cmath
import scipy  # re - для работы с регулярными выражениями
import numpy as np
import matplotlib
from scipy import integrate
from PIL import Image  # для выввода изображения
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib as mpl

# QDesktopWidget предоставляет информацию о компьютере пользователя
# QMainWindow - создает статус бар

import random
from urllib import request
import urllib.parse as parse
import json
import time
from computer import *
import diffraction
import email_module
import sys
import os
import requests


def load_files_to_db(url,path,pk):
    included_extenstions = ['dat','gif','pdf','docx']
    file_names = [fn for fn in os.listdir(path+'/')
                    if any(fn.endswith(ext) for ext in included_extenstions)]
    print('найдено файлов: ',len(file_names))   
    files = {}

    for i in file_names:
        f = path+'/' + str(i)
        files[i] = open(f, 'rb')
    print(files)
    values = {'pk':pk}
    r = requests.post(url, files=files, data = values)
    print('файлы отправлены')
    return r

def check_updates():

    with open('version.time','r') as ver:
        ver_old = ver.read()
    r = requests.get('https://atknin:24fdf9551e219c7103993b34050afc0f4141d053@api.github.com/repos/atknin/x-rays-computer/events')
    string = r.text
    created_at = json.loads(string)[0]['created_at']
    if ver_old != created_at:
        with open('version.time','w') as ver:
            ver.write(created_at)
            print('need update')
        return True
    else:
        return False


def check_tasks_base(url):
    try:
        if check_updates():
            os.system('git pull')
            os.system('python3 main.py')
            sys.exit()
    except Exception as e:
        print('не удалось проверить обновлениеы')
    
    try:
        # проверка на наличие задачи в базе
        payload = {'check': comp}
        data = parse.urlencode(payload)
        f = request.urlopen(url + "?" + data)
        while f.status !=200: 
            f = request.urlopen(url + "?" + data)
            time.sleep(10)
        string = f.read().decode('utf-8')
        son_obj = {}
        son_obj = json.loads(string)

        # если нет рсчетов в базе
        if son_obj['status'] == 'Nodata':
            print('[.]')
            time.sleep(100)
            check_tasks_base(url)

        # если есть и их тип определен
        elif (son_obj['type']==0 or son_obj['type']==1) and ('JSON' in son_obj):
            return son_obj

        # # загрузка Расчета дифракции на сайт
        # elif son_obj['type']==2:
        #     print('загрузка Расчета дифракции на сайт')
        # # повторная отправка результатов расчет 
        # elif son_obj['type']==3:
        #     try:
        #         print('отправка расчета по почте')
        #         path = os.path.dirname(os.path.abspath(__file__))+'/results/'+str(son_obj['pk'])
        #         email = son_obj['email']
        #         title = 'xrayd: повторная отправка'
        #         text = str(open(path+'/info.dat','r').read())
        #         email_module.sendEmail(class_compute.return_path(),email,title,text)
        #     except Exception as e:
        #         print('ошибка при повторной отправке параметров')
        
        else:
            print('check_tasks_base else')
            time.sleep(10)
            check_tasks_base(url)
    except Exception as e:
        print(e)
        print('Ошибка в check_tasks_base')

    time.sleep(10)
    check_tasks_base(url)



if __name__ == "__main__":
    print('the program is started!')
    url = 'http://62.109.0.242/diffraction/compute/'
    url_file = 'http://62.109.0.242/diffraction/load_files/'
    while True:
        # ff = open('text_json_data','w')
        while True:
            try:
                json_data = check_tasks_base(url)
                json_data['JSON']
                break
            except Exception as e:
                pass
       
        print(json_data)
        # ff.write(str(json_data))
        # break
        class_compute = diffraction.compute(json_data)
        print(1000*'*','\n\n',class_compute.show_parametrs(),100*'-')

        # расчитать алгоритм
        try:
            status = class_compute.start_algoritm()
        except Exception as e:
            print('[!!!] неизвестная ошибка - там где ее не должно быть')
        print('status: ',status)
        if status==200:
            # отпрвить результаты на почту
            title = 'успешно: ' + class_compute.return_input_data()['id_comment_calc']
            text = class_compute.show_parametrs()
            email = class_compute.return_input_data()['id_email']
            email_module.sendEmail(class_compute.return_path(),email,title,text)
            # отпрвить файлы на сервер
            load_files_to_db(url_file,class_compute.return_path(),json_data['pk'])
            # отпрвить отчет на сервер
            payload = {'complited': json_data['pk']}
            payload['pc'] = comp
            data = parse.urlencode(payload)
            f = request.urlopen(url + "?" + data)
            while f.status !=200: 
                f = request.urlopen(url + "?" + data)
                time.sleep(10)
            print('Сообщили об окончании расчета')

        elif status ==155: # остановка расчета
            # отпрвить отчет на сервер
            payload = {'error_during_compute': json_data['pk'], 'text_error': 'stoped'}
            payload['pc'] = comp
            data = parse.urlencode(payload)
            f = request.urlopen(url + "?" + data)
            kk = 0
            while kk<10: 
                f = request.urlopen(url + "?" + data)
                time.sleep(10)
                kk+=1
            print('Сообщили об остановке расчета расчета')

        elif status ==500:
            print('ОШИБКА:')
            er_text = class_compute.return_status()
            print(er_text)
            payload = {'error_during_compute': json_data['pk'], 'text_error': 'ERROR 2: ' + er_text}
            payload['pc'] = comp
            data = parse.urlencode(payload)
            f = request.urlopen(url + "?" + data)
            while f.status !=200: 
                f = request.urlopen(url + "?" + data)
                time.sleep(10)

        elif status ==404:
            print('ОШИБКА: не существующий алгоритм')
        else:
            print('ОШИБКА: неизвестная ошибка ')
        time.sleep(1)




