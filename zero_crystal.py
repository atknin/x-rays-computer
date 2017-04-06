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

from functions import (g_lambd, gauss, frenel_slit, slit_extensive_source)


def do_it(input_data):
    print('do_it for:')
    msge = {}
    print(input_data)
    path = os.path.dirname(os.path.abspath(__file__))+'/results/'
    wavelength_1 = float(input_data['anod1']) * 1e-10
    wavelength_2 = float(input_data['anod2']) * 1e-10
    S1 = float(input_data['input_size_slit1']) * \
        1e-3  # S1, S2 - ширина колимирующих щелей
    S2 = float(input_data['input_size_slit2']) * 1e-3
    # L1, L2 - оптические расстояния между щелей и рентгеновской трубкой
    L1x = float(input_data['input_l_slit1'])
    L2x = float(input_data['input_l_slit2'])
    sigma = float(input_data['source_divergence_arc'])
    try:
        sigma_metr = float(input_data['source_divergence_mmetr']) * 1e-3
    except Exception as e:
        sigma_metr = 0.5*1e-3
        print('sigma metr не определена, 0.5 по умолчанию')
    name_gif = input_data['name_result']
    slits = [1, 1, 1, 1]  # 1(движется)  и 2(не движется) щели
    # 2 щель (движется)- перед детектором
    slits[0] = -math.degrees(math.atan(S2/2/L2x))*3600
    # 2 щель(движется)- перед детектором
    slits[1] = math.degrees(math.atan(S2/2/L2x))*3600
    slits[2] = -math.degrees(math.atan(S1/2/L1x))*3600  # 1 щель(не движется)
    slits[3] = math.degrees(math.atan(S1/2/L1x))*3600  # 1 щель(не движется)
    shagi_po_Dtheta_uvellichenie = [-20, 20, math.radians(0.5/3600)]
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
    svertka_plot_shkala = 'Nonlog'
    #--------------------------------------------шаг по длине волны-----------
    try:
        shag_itta = math.radians(5/3600) * float(input_data['step_lambda'])
    except Exception as e:
        shag_itta = math.radians(5/3600)
        print('shag_itta не определен')

    itta_1 = 0.996  # предел интегрирования от
    itta_2 = 1.01  # предел интегрирования до
    int((itta_2 - itta_1)/shag_itta)
    #--------------------------------------------шаг по углу, разлет от источн

    try:
        shag_teta = math.radians(float(1/3600))/8 * \
                                                         float(
                                                             input_data['step_teta'])
    except Exception as e:
        shag_teta = math.radians(float(1/3600))/8
        print('shag_teta не определен')
    math.radians(surf_plot_x_lim[0]/3600)
    teta_2 = math.radians(surf_plot_x_lim[1]/3600)
    # -----------------------------------------------------Шаг, поворот образц
    int(2*teta_2/shag_teta)
    dTeta = dTeta_st = math.radians(surf_plot_x_lim[0]/3600)
    dTeta_end = math.radians(surf_plot_x_lim[1]/3600)

    try:
        dTeta_shag = math.radians(float(input_data['step_shag_teta'])/3600)
    except Exception as e:
        dTeta_shag = math.radians(10/3600)
        print('dTeta_shag не определен')
    print('параметры успешно определены')

    # -----------Аппаратная функция-------------------

    def gif(path_gif):
        filenam = os.listdir(path_gif)
        filenames_a = sorted(filenam)
        filenames = filter(lambda x: x.endswith('.png'), filenames_a)
        images = []
        i = 0
        for filename in filenames:
            print(path_gif+str(i)+'.png')
            images.append(imageio.imread(path_gif+str(i)+'.png'))
            i += 1
        print('!creating: ... |', path + name_gif + '.gif')
        imageio.mimsave(path + name_gif + '.gif', images)
        print('!done:', path + name_gif + '.gif')


#-------------------вресмя уменьшилось на 10 процентов
    def svertka(x_itta, y_teta, z_intese, sdvig=0):
        dlina = len(z_intese)
        dlina_2 = len(z_intese[0])
        suma = 0
        for i in range(dlina):
            for j in range(dlina_2):
                # if (slits[2]*10)<y_teta[i][j]<(slits[3]*10):
                if (slits[2]) < y_teta[i][j] < (slits[3]):
                    if (slits[0]+sdvig) < y_teta[i][j] < (slits[1]+sdvig):
                        suma += z_intese[i][j]
        return suma

    def PLOT_all(X, Y, Z, dTeta, sdvig, svert_x, svert_y, i):
        plt.style.use('ggplot')
        ax1 = plt.subplot(2, 1, 2)
        mpl.rcParams.update({'font.size': 15})
        p1 = plt.pcolormesh(Y, X, Z, shading='gouraud',
                            cmap='jet', vmin=-4, vmax=0)
        ax1.broken_barh([(surf_plot_x_lim[0], slits[2]-surf_plot_x_lim[0]), (slits[3],
                                                                             surf_plot_x_lim[1]-slits[3])], (0.5, 0.5), facecolors='red', alpha=0.2)
        ax1.broken_barh([(surf_plot_x_lim[0], slits[0]-surf_plot_x_lim[0]+sdvig), (slits[1] +
                                                                                   sdvig, surf_plot_x_lim[1]-slits[1]-sdvig)], (0.5, 0.5), facecolors='grey', alpha=0.2)
        ax1.broken_barh([(slits[0]+sdvig-0.25+(slits[1] - slits[0])/2,
                          0.5)], (0.5, 0.5), facecolors='red', alpha=0.4)
        plt.xlim(surf_plot_x_lim[0], surf_plot_x_lim[1])
        plt.ylim(surf_plot_y_lim[0], surf_plot_y_lim[1])
        plt.colorbar()
        plt.subplot(2, 1, 1)
        plt.plot(svert_x, svert_y)
        plt.xlim(svertka_plot_x_lim[0], svertka_plot_x_lim[1])
        plt.savefig(path + name_gif + '/'+str(i) + '.png', bbox_inches='tight')
        plt.close()

    def cli_progress_test(end_val, bar_length=20):
        percent = end_val
        hashes = '#' * int(round(percent * bar_length)/100)
        spaces = ' ' * (bar_length - len(hashes))
        sys.stdout.write("\rPercent: [{0}] {1}%".format(
                hashes + spaces, int(round(percent))))
        sys.stdout.flush()

    def one(dTeta):  # скан одной щелью относительно второй
        i = 0
        sv_x = []
        sv_y = []
        f = open(path + name_gif + '.dat', 'w')

        while dTeta <= dTeta_end:
            cli_progress_test((dTeta-dTeta_st+dTeta_shag) /
                              (dTeta_end - dTeta_st)*100)
        # 1-------------------------------------------------------------------------------------------------------------------
            itta = itta_1
            x_itta = []
            y_teta = []
            z_intese = []
            z_intese_lin = []
            while itta <= itta_2:
                #----3---------------------------------------------------------
                teta = -teta_2
                x_promegutochn = []
                y_promegutochn = []
                z_promegutochn = []
                z_promegutochn_lin = []
                while teta <= teta_2:
                    P = g_lambd(itta, wavelength_1, wavelength_2) * \
                                            gauss(
                                                sigma, 0, math.degrees(teta)*3600)
                    x_promegutochn.append(itta*wavelength_1*1e10)
                    y_promegutochn.append(math.degrees(teta)*3600)
                    z_promegutochn.append(math.log10(P))
                    z_promegutochn_lin.append(P)
                    teta += shag_teta

                #----3---------------------------------------------------------
                x_itta.append(x_promegutochn)
                y_teta.append(y_promegutochn)
                z_intese.append(z_promegutochn)
                z_intese_lin.append(z_promegutochn_lin)
                itta += shag_itta
                #-2------------------------------------------------------------

            sdvigka = -2*(math.degrees(dTeta)*3600)
            f.write('%14.8f' % sdvigka)
            f.write('%14.8f' % svertka(x_itta, y_teta, z_intese_lin, sdvigka))
            f.write('\n')

            if svertka_plot_shkala == 'log':
                sv_y.append(math.log10(0.00000000000001 +
                                       svertka(x_itta, y_teta, z_intese_lin, sdvigka)))
            else:
                sv_y.append(svertka(x_itta, y_teta, z_intese_lin, sdvigka))
            sv_x.append(sdvigka)
            PLOT_all(x_itta, y_teta, z_intese,
                     (math.degrees(dTeta)*3600), sdvigka, sv_x, sv_y, i)
            i += 1
            if shagi_po_Dtheta_uvellichenie[0] <= (math.degrees(dTeta)*3600) <= shagi_po_Dtheta_uvellichenie[1]:
                dTeta += shagi_po_Dtheta_uvellichenie[2]
            else:
                dTeta += dTeta_shag
        f.close()

    def new(dTeta):  # скан одной щелью относительно второй
        i = 0
        f = open(path + name_gif + '.dat', 'w')



        while dTeta <= dTeta_end:
            cli_progress_test((dTeta-dTeta_st+dTeta_shag) /
                              (dTeta_end - dTeta_st)*100)
            teta_1 = (-(sigma_metr + S2)/2 )/L2x - dTeta
            teta_2 = ((sigma_metr + S2)/2 )/L2x - dTeta
        # 1-------------------------------------------------------------------------------------------------------------------
            itta = itta_1
            sdvigka = -(math.degrees(dTeta)*3600)

            P = 0
            while itta <= itta_2:
                #----3---------------------------------------------------------
                teta = teta_1
                while teta <= teta_2:
                    P += g_lambd(itta, wavelength_1, wavelength_2) * \
                                            gauss(sigma, 0, math.degrees(teta)*3600) * \
                                            slit_extensive_source(math.degrees(teta)*3600,sdvigka,L1x,L2x,S1,S2,sigma_metr)
                    teta += shag_teta

                #----3---------------------------------------------------------
                itta += shag_itta
                #-2------------------------------------------------------------

            f.write('%14.8f' % sdvigka)
            f.write('%14.8f' % P)
            f.write('\n')
            i += 1

            dTeta += dTeta_shag
        f.close()

    if not os.path.exists(path + name_gif + '/'):
        os.makedirs(path + name_gif + '/')
        print('создаем папку: ' + path + name_gif + '/')
    print('начался расчет...')
    msge['title'] = 'Расчет: ' + str(input_data['id_comment_calc'])
    email_module.notification(
            'Расчет начался' + str(input_data['id_comment_calc']))
    if input_data['slits'] == 'new':
        print('new_slits')
        new(dTeta)
    else:
        one(dTeta)
        print('сбока анимации...')
        gif(path + name_gif + '/')
        msge = {}
        msge['gif'] = path + name_gif + '.gif'

    email_module.notification(
            'Расчет окончен для '+str(input_data['id_email']))
    msge['text'] = 'Источник (р.трубка): (' + str(wavelength_1) + \
        '; ' + str(wavelength_2) + '). Input Data: ' + str(input_data)
    msge['dat'] = []
    msge['dat'].append(path + name_gif + '.dat')
    email_module.sendEmail(msge, input_data['id_email'])
