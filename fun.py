import sys
from functions import *
import matplotlib as mpl

import math,os,imageio
import cmath
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import numpy as np
from double_crystal import do_it
from decimal import Decimal

# from smsc_api import *
# smsc = SMSC()
#
# to = '+79151322437'
# to = '+79152369304'
#
# r = smsc.send_sms("+79152369304", "Я тебя люблю, спокойной ночки, кис!")
# balance = smsc.get_balance()
# print(r)
# print(balance)
# # ...
# r = smsc.send_sms("79999999999", "http://smsc.ru\nSMSC.RU", query="maxsms=3")
# ...
# r = smsc.send_sms("79999999999", "0605040B8423F0DC0601AE02056A0045C60C036D79736974652E72750001036D7973697465000101", format=5)
# ...
# r = smsc.send_sms("79999999999", "", format=3)
# ...
# r = smsc.get_sms_cost("79999999999", "Вы успешно зарегистрированы!")
# ...
# r = smsc.get_status(12345, "79999999999")
# ...
# balance = smsc.get_balance()
# ...
# # отправка SMS через e-mail
# smsc.send_sms_mail("79999999999", "Ваш пароль: 123")
# ...
path = "/Users/Atknini/Desktop/single slit"

def Plot(x,y,i, method,df,ss1,ss2,maxa):
    axes = plt.gca()
    plt.plot(x, y, 'red', linewidth=3.0)
    # plt.plot(exp_x, exp_y, 'g.', linewidth=1.0, label = 'эксперимент')
    plt.grid(True)
    #plt.title('s1='+str(round(S1*1000000,0))+', s2 =' + str(round(S2*1000000,0)))
    plt.xlabel('$ \Theta, угл. сек. $', fontsize=25)
    plt.ylabel('$ I, отн. ед. $', fontsize=25)
    # axes.set_ylim([0,maxa])
    plt.title('S2 = {} mcm'.format(ss2*1000), loc='right')
    plt.title('delta = {} mcm'.format(df*1000), loc='left')
    plt.title('S1 = {} mcm'.format(ss1*1000), loc='center')
    # axes.set_ylim([0,0.0001])
    plt.legend(bbox_to_anchor=(1, 1), loc=1, borderaxespad=0.)
    if method =='show':
        plt.show()
    else:

        plt.savefig(path + '/'+str(i) + '.png', bbox_inches='tight')
        plt.close()

S = 0.2 * 1e-3
sigma = 0.1 * 1e-3
sdvigka = 0
L1 = 0.57
L2 = 1.005

teta_shag = 0.01
delta = [0.1*10**-3]
ssl = [0.2*10**-3,0.4*10**-3]
kk = 0
for df in delta:
    for ss1 in ssl:
        for ss2 in ssl:
            teta_2 = 300
            teta_1 = -300
            teta = teta_1
            x = []
            y = []
            while teta <= teta_2:
                teta_radians = math.radians(teta/3600)
                P = slit_extensive_source(teta,sdvigka,L1,L2,ss1,ss2,df)
                # P = slit_extensive_source(teta,sdvigka,L1,L2,S1,S2,sigma)*gauss(700, 0, teta)
                # P = apparatnaya(teta_radians,teta_1,teta_2,L1,L2,S1,S2,sigmaX = sigma)
                x.append(teta)
                y.append(100000*P)
                teta += teta_shag
            Plot(x,y,kk,'show',df,ss1,ss2,max(y))
            kk+=1
