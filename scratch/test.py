# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from functions import *
import matplotlib as mpl

import math,os,imageio
import cmath
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import numpy as np
from double_crystal import do_it
from fun import *
from decimal import Decimal
a = [1, 2]
b = a
a = []

a = [1, 2]
b = a
del a[:], b[:]

dTeta = 0


teta_shag = 0.1
itta = 1
X0 = complex(-31.7799 + 0.1558j)*1e-7
Xh = complex(19.175 + 0.1505j)*1e-7
tetaprmtr_deg = 10.6436
# #-------si 440----------------
# X0 = complex(-31.7799 + 0.1558j)*1e-7
# Xh = complex(12.0462 + 0.1358j)*1e-7
# tetaprmtr_deg = 21.6785

fi = 0

sigma = 500
extintion = 11.572e-6
l_plenka = 1e-3
da_plenka = 0.8
fwhm = math.radians(2.18/3600)
amorphizaciya = 1
x = []
y = []
ynorm = []
L1 = 0.57
L2 = 1.005
S1 = 0.2 * 1e-3
S2 = 0.4 * 1e-3
sigma = 0.1 * 1e-3

surf_plot_x_lim = [-300,300]
surf_plot_y_lim = [0.706,0.716]
# surf_plot_y_lim = [1.537,1.547]
# surf_plot_y_lim = [0.706-0.01,1.547+0.01]
# path = '/Users/Atknini/GDrive/work.science/Conference and Schools/Ломоносов 2017/move'
def save_3d_file(path,x,y,z):
    with open(path, 'w') as f:
        for i, j, k in zip(x, y, z):
            f.write("{:.10f}     {:.10f}     {:.10f}\n".format(i,j,k))

def save_2d_file(path,x,y):
    with open(path, 'w') as f:
        for i, j in zip(x, y):
            f.write("{:.10f}     {:.10f}\n".format(i,j))

def Plot(x,y,i, method):
    axes = plt.gca()
    plt.plot(x, y, 'red', linewidth=3.0)
    # plt.plot(exp_x, exp_y, 'g.', linewidth=1.0, label = 'эксперимент')
    plt.grid(True)
    #plt.title('s1='+str(round(S1*1000000,0))+', s2 =' + str(round(S2*1000000,0)))
    plt.xlabel('$ \Theta, угл. сек. $', fontsize=25)
    plt.ylabel('$ I, отн. ед. $', fontsize=25)
    # axes.set_ylim([0,90])
    # axes.set_ylim([0,0.0001])
    plt.legend(bbox_to_anchor=(1, 1), loc=1, borderaxespad=0.)
    if method =='show':
        plt.show()
    else:

        plt.savefig(path + '/'+str(i) + '.png', bbox_inches='tight')
        plt.close()


def PLOT_surf(X, Y, Z, i,method,n):
    plt.style.use('ggplot')
    ax1 = plt.subplot(1, 1, 1)
    mpl.rcParams.update({'font.size': 15})
    p1 = plt.pcolormesh(Y, X, Z, shading='gouraud',
                        cmap='jet', vmin=n, vmax=-5)
    plt.xlim(surf_plot_x_lim[0], surf_plot_x_lim[1])
    plt.ylim(surf_plot_y_lim[0], surf_plot_y_lim[1])
    plt.colorbar()
    if method == 'show':
        plt.show()
    else:
        plt.savefig(path  + '_SURF_'+str(i) + '.png', bbox_inches='tight')
        plt.close()


def slits_sh(name):
    sdvigka = 0
    sdvigka_rad = math.radians(sdvigka/3600)
    # teta_1 = -math.degrees((S2+sigma)/(2*(L2)))*3600 + 3*sdvigka
    # teta_2 = math.degrees((S2+sigma)/(2*(L2)))*3600 + 3*sdvigka
    teta_2 = 300
    teta_1 = -300
    teta = teta_1
    x = []
    y = []
    while teta <= teta_2:
        teta_radians = math.radians(teta/3600)
        P = slit_extensive_source(teta,sdvigka,L1,L2,S1,S2,sigma)
        # P = slit_extensive_source(teta,sdvigka,L1,L2,S1,S2,sigma)*gauss(700, 0, teta)
        # P = apparatnaya(teta_radians,teta_1,teta_2,L1,L2,S1,S2,sigmaX = sigma)
        x.append(teta)
        y.append(100000*P)
        teta += teta_shag
    p = '/Users/Atknini/GDrive/work.science/Publ./1_Apparat_and_maps_ost_diploma/graph/2slits/'+ name + '.dat'
    save_2d_file(p,x,y)
    # Plot(x,y,0,'show')



def svertka():
    sdvigka = 60
    i = 0
    while sdvigka>-60:
        teta_start = teta = math.degrees((-(sigma + S2)/2 )/L2)*3600 + 4*sdvigka
        teta_end = math.degrees(((S2+sigma)/2 )/L2)*3600 + 4*sdvigka
        graph_x = []
        graph_y = []
        while teta <= teta_end:
            teta_radians = math.radians(teta/3600)
            P += slit_extensive_source(teta,sdvigka,L1,L2,S1,S2,sigma)
            graph_x.append(teta)
            graph_y.append(slit_extensive_source(teta,sdvigka,L1,L2,S1,S2,sigma))
            teta += teta_shag


        Plot(graph_x,graph_y,i)
        x.append(sdvigka)
        y.append(P)
        sdvigka-=1
        i+=1
        print(i)
        gif(path)

def spectr_teta(i):
    itta_1 = teta = surf_plot_y_lim[0]  # предел интегрирования от
    itta_2 = surf_plot_y_lim[1]  # предел интегрирования до
    itta = itta_1
    shag_itta = (itta_2-itta_1)/700
    teta_start = teta = surf_plot_x_lim[0]
    teta_end = surf_plot_x_lim[1]
    teta_shag = (teta_end - teta_start)/1000

    graph_x = []
    graph_y = []
    graph_z = []

    file_x = []
    file_y = []
    file_z = []
    while itta <= itta_2:
        #----3---------------------------------------------------------
        teta = teta_start
        x = []
        y = []
        z = []
        while teta <= teta_end:
            # P = 1e13*g_lambd(itta/(wavelength_1*1e10), wavelength_1, wavelength_2)*slit_extensive_source(teta,0,L1,L2,S1,S2,sigma) * gauss(400, 0, teta)*monohromator_curve(math.radians(teta/3600), itta/(wavelength_1*1e10), X0, Xh, tetaprmtr_deg, 0) #5
            # P = 1e15*g_lambd(itta/(wavelength_1*1e10), wavelength_1, wavelength_2)*slit_extensive_source(teta,0,L1,L2,S1,S2,sigma) * gauss(400, 0, teta)*monohromator_curve(math.radians(teta/3600), itta/(wavelength_1*1e10), X0, Xh, tetaprmtr_deg, 0) *sample_curve(math.radians(0/3600), math.radians(teta/3600), itta/(wavelength_1*1e10), X0, Xh, tetaprmtr_deg, 0) #6.1
            # P = 1e15*g_lambd(itta/(wavelength_1*1e10), wavelength_1, wavelength_2)*slit_extensive_source(teta,0,L1,L2,S1,S2,sigma) * gauss(400, 0, teta)*monohromator_curve(math.radians(teta/3600), itta/(wavelength_1*1e10), X0, Xh, tetaprmtr_deg, 0) *sample_curve(math.radians(270/3600), math.radians(teta/3600), itta/(wavelength_1*1e10), X0, Xh, tetaprmtr_deg, 0) #6.2
            # P = 1e17*g_lambd(itta/(wavelength_1*1e10), wavelength_1, wavelength_2) * slit_extensive_source(teta,0,L1,L2,S1,S2,sigma) * gauss(400, 0, teta)*monohromator_curve(math.radians(teta/3600), itta/(wavelength_1*1e10), X0, Xh, tetaprmtr_deg, 0) * sample_curve(math.radians(0/3600), math.radians(teta/3600), itta/(wavelength_1*1e10), X0, Xh, 21.6, 0) #7.1
            P = 1e17*g_lambd(itta/(wavelength_1*1e10), wavelength_1, wavelength_2) * slit_extensive_source(teta,0,L1,L2,S1,S2,sigma) * gauss(400, 0, teta)*monohromator_curve(math.radians(teta/3600), itta/(wavelength_1*1e10), X0, Xh, tetaprmtr_deg, 0) * sample_curve(math.radians(0/3600), math.radians(teta/3600), itta/(wavelength_1*1e10), X0, Xh, 33.6, 0) #7.2
            # P = g_lambd(itta/(wavelength_1*1e10), wavelength_1, wavelength_2) * gauss(400, 0, teta)*monohromator_curve(math.radians(teta/3600), itta/(wavelength_1*1e10), X0, Xh, tetaprmtr_deg, 0)*sample_curve(math.radians(0/3600), math.radians(teta/3600), itta/(wavelength_1*1e10), X0, Xh, tetaprmtr_deg, 0)
            # P = 1e10*gauss(600, 0, teta)*slit_extensive_source(teta,0,L1,L2,1,1,sigma)*monohromator_curve(math.radians(teta/3600), itta/(wavelength_1*1e10), X0, Xh, tetaprmtr_deg, (tetaprmtr_deg-0.001))*sample_curve(math.radians(50/3600), math.radians(teta/3600),itta/(wavelength_1*1e10), X0, Xh, tetaprmtr_deg, 0)*g_lambd(itta/(wavelength_1*1e10), wavelength_1, wavelength_2)
            # P = 1e10*gauss(600, 0, teta)*slit_extensive_source(teta,0,L1,L2,1,1,sigma)*g_lambd(itta/(wavelength_1*1e10), wavelength_1, wavelength_2)*monohromator_curve(math.radians(teta/3600), itta/(wavelength_1*1e10), X0, Xh, tetaprmtr_deg, -(tetaprmtr_deg-0.1))
            # P = 10000*gauss(600, 0, teta) * g_lambd(itta/(wavelength_1*1e10), wavelength_1, wavelength_2) * slit_extensive_source(teta,0,L1,L2,S1,S2,sigma)*monohromator_curve(math.radians(teta/3600), itta/(wavelength_1*1e10), X0, Xh, tetaprmtr_deg, 0)
            # P = 10000*monohromator_curve(math.radians(teta/3600), itta/(wavelength_1*1e10), X0, Xh, tetaprmtr_deg, 0)
            # P = 10000*gauss(600, 0, teta) * g_lambd(itta/(wavelength_1*1e10), wavelength_1, wavelength_2) * slit_extensive_source(teta,0,L1,L2,S1,S2,sigma)
            x.append(teta)
            y.append(itta)
            z.append(math.log10(P+1e-20))
            # z.append(round(P,7))

            file_x.append(teta)
            file_y.append(itta)
            file_z.append(round(math.log10(P+1e-5),5))
            # file_z.append(round(P,5))
            teta += teta_shag

        #----3---------------------------------------------------------
        graph_x.append(x)
        graph_y.append(y)
        graph_z.append(z)
        itta += shag_itta
        #-2------------------------------------------------------------
    save_3d_file(path+str(i)+'.dat',file_x,file_y,file_z)
    PLOT_surf(graph_y, graph_x, graph_z, i,'s',-15)

#
wavelength_1 = 0.7093*1e-10
wavelength_2 = 0.714*1e-10
path = '/Users/Atknini/GDrive/work.science/Publ./1_Apparat_and_maps_ost_diploma/graph/scryst/'
spectr_teta('#7_2')

