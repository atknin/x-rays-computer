# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import math
import cmath
import os
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
from numpy import random

plt.style.use('ggplot')

from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from numpy import array

from matplotlib import animation
from matplotlib import cm
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import LinearLocator
from numpy import array
import matplotlib.colors as colors
from PIL import Image
from PIL import ImageSequence
import imageio
# import psutil

import email_module


from functions import *


def do_it(input_data):
    print('do_it for:')
    print(input_data)
    path = input_data['path'] + '/'
    wavelength_1 = float(input_data['anod1']) * 1e-10
    wavelength_2 = float(input_data['anod2']) * 1e-10

    sigma = float(input_data['source_divergence_arc'])
    try:
        sigma_metr = float(input_data['source_divergence_mmetr']) * 1e-3
    except Exception as e:
        sigma_metr = 0.2*1e-3
        print('sigma metr не определена, 0.2 по умолчанию')
    S1 = float(input_data['input_size_slit1']) * 1e-3
    S2 = float(input_data['input_size_slit2']) * 1e-3 *100
          # S1, S2 - ширина колимирующих щелей
    # L1, L2 - оптические расстояния между щелей и рентгеновской трубкой
    L1x = float(input_data['input_l_slit1'])
    L2x = float(input_data['input_l_slit2'])
    X0_1 = complex(input_data['X0_1'])*1e-7
    Xh_1 = complex(input_data['Xh_1'])*1e-7
    X0_2 = complex(input_data['X0_2'])*1e-7
    Xh_2 = complex(input_data['Xh_2'])*1e-7
    X0_3 = complex(input_data['X0_3'])*1e-7
    Xh_3 = complex(input_data['Xh_3'])*1e-7

    bragg_1 = float(input_data['bragg_1'])
    bragg_2 = float(input_data['bragg_2'])
    bragg_3 = float(input_data['bragg_3'])

    fi_monohrom = float(input_data['fi_1'])
    fi_sample = float(input_data['fi_2'])
    fi_analayzer = float(input_data['fi_3'])

    name_gif = str(input_data['name_result'])
    slits = [1, 1, 1, 1]  # 1(движется)  и 2(не движется) щели
    # 2 щель (движется)- перед детектором
    slits[0] = -math.degrees(math.atan(S2/2/L2x))*3600
    # 2 щель(движется)- перед детектором
    slits[1] = math.degrees(math.atan(S2/2/L2x))*3600
    slits[2] = -math.degrees(math.atan(S1/2/L1x))*3600  # 1 щель(не движется)
    slits[3] = math.degrees(math.atan(S1/2/L1x))*3600  # 1 щель(не движется)
    surf_plot_x_lim = [float(input_data['teta_start']),
                       float(input_data['teta_end'])]
    left = float(input_data['anod1']) - 0.5 * \
        abs(float(input_data['anod2']) - float(input_data['anod1']))
    right = float(input_data['anod2']) + 0.5 * \
        abs(float(input_data['anod2']) - float(input_data['anod1']))
    if wavelength_2 > wavelength_1:
        surf_plot_y_lim = [left, right]
    else:
        surf_plot_y_lim = [right, left]
    svertka_plot_x_lim = [float(input_data['teta_start']), float(
            input_data['teta_end'])]  # для линейной шкалы
    svertka_plot_shkala = input_data['logarifm_scale']
    #--------------------------------------------шаг по длине волны-----------
    try:
        shag_itta = math.radians(5/3600) * float(input_data['step_lambda'])
    except Exception as e:
        shag_itta = math.radians(5/3600)
        print('shag_itta не определен')
    itta_1 = 0.996  # предел интегрирования от
    itta_2 = 1.01  # предел интегрирования до
    #--------------------------------------------шаг по углу, разлет от источн
    try:
        shag_teta = math.radians(float(1/3600))/8 * \
                                                         float(
                                                             input_data['step_teta'])
    except Exception as e:
        shag_teta = math.radians(float(1/3600))/8
        print('shag_teta не определен')
    teta_1 = -math.atan(S1/2/L1x)
    teta_2 = -teta_1
    # -----------------------------------------------------Шаг, поворот образц
    dTeta = dTeta_st = math.radians(surf_plot_x_lim[0]/3600)
    dTeta_end = math.radians(surf_plot_x_lim[1]/3600)
    try:
        dTeta_shag = math.radians(float(input_data['step_shag_teta'])/3600)
    except Exception as e:
        dTeta_shag = math.radians(2/3600)
        print('dTeta_shag не определен')
    print('параметры успешно определены: double crystla experiment')


    def cli_progress_test(end_val, bar_length=20):
        percent = end_val
        hashes = '#' * int(round(percent * bar_length)/100)
        spaces = ' ' * (bar_length - len(hashes))
        sys.stdout.write("\rPercent: [{0}] {1}%".format(
                hashes + spaces, int(round(percent))))
        sys.stdout.flush()

    def theta(dTeta):  # скан одной щелью относительно второй
        i = 0

        f = open(path + name_gif + '.dat', 'w')
        epsilon = dTeta_st
        while epsilon<=dTeta_end:
            dTeta = dTeta_st
            # Обновляем прогресс бар
            prcents = (dTeta-dTeta_st+dTeta_shag) / (dTeta_end - dTeta_st)*100
            try:
                payload = {'progress':input_data['name_result'],'value':int(prcents)}
                get_request('http://62.109.0.242/diffraction/compute/',payload)
            except Exception as e:
                print('ошибка обновления прогресс бара: ',e)
            cli_progress_test(prcents)
            
            while dTeta <= dTeta_end:
            # 1-------------------------------------------------------------------------------------------------------------------
                itta = itta_1
                P = 0
                while itta <= itta_2:
                    # 3-----------------------------------------------------------------------------------------------------------
                    teta = teta_1
                    while teta <= teta_2:
                        P += g_lambd(itta, wavelength_1, wavelength_2)*gauss(sigma, 0, math.degrees(teta)*3600)*sample_curve(
                                dTeta, teta, itta, X0_2, Xh_2, bragg_2, fi_sample)*monohromator_curve(teta, itta, X0_1, Xh_1, bragg_1, fi_monohrom)*analyzer_curve(epsilon,dTeta,teta, itta, X0_3, Xh_3, bragg_3, fi_analayzer)
                        teta += shag_teta
                    #----3---------------------------------------------------------
                    itta += shag_itta
                    #-2------------------------------------------------------------
                f.write('%14.8f' % (math.degrees(dTeta)*3600))
                f.write('%14.8f' % (math.degrees(epsilon)*3600))
                f.write('%14.8f' % P)
                f.write('\n')
                i += 1
                dTeta += dTeta_shag
            epsilon += dTeta_shag
        f.close()

    print('начался расчет...')
    if not os.path.exists(path + name_gif + '/'):
        os.makedirs(path + name_gif + '/')
        print('создаем папку: ' + path + name_gif + '/')

    email_module.notification(
            " Старт: " + str(input_data['id_comment_calc']))
    theta(dTeta)
    email_module.notification(
            'Расчет окончен для '+str(input_data['id_email']))


