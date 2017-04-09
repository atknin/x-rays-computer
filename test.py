from functions import sample_curve
from functions import sample_curve_broken
from functions import sample_curve_broken_integrate
from functions import slit_extensive_source
import math,os,imageio
import cmath
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import numpy as np
from double_crystal import do_it
a = [1, 2]
b = a
a = []
print(a)

a = [1, 2]
b = a
del a[:], b[:]
print(a, b)

dTeta = 0


teta_shag = 0.1
itta = 1
X0 = complex(-31.7799 + 0.1558j)*1e-7
Xh = complex(19.175 + 0.1505j)*1e-7
tetaprmtr_deg = 10.6436
fi = 0

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
S1 = 0.05 * 1e-3
S2 = 0.05 * 1e-3
sigma = 0.2 * 1e-3


# sdvigka = 0
# teta_start = teta = math.degrees((-(sigma + S2)/2 )/L2)*3600 + 2*sdvigka
# teta_end = math.degrees(((S2+sigma)/2 )/L2)*3600 + 2*sdvigka
# while teta <= teta_end:
#     teta_radians = math.radians(teta/3600)
#     P = slit_extensive_source(teta,sdvigka,L1,L2,S1,S2,sigma)
#     x.append(teta)
#     y.append(P*100000/8)
#     teta += teta_shag

path = '/Users/Atknini/GDrive/work.science/Conference and Schools/Ломоносов 2017/move'
def Plot(x,y,i):
    axes = plt.gca()
    plt.plot(x, y, 'red', linewidth=3.0)
    # plt.plot(exp_x, exp_y, 'g.', linewidth=1.0, label = 'эксперимент')
    plt.grid(True)
    #plt.title('s1='+str(round(S1*1000000,0))+', s2 =' + str(round(S2*1000000,0)))
    plt.xlabel('$ \Theta, угл. сек. $', fontsize=25)
    plt.ylabel('$ I, отн. ед. $', fontsize=25)
    axes.set_xlim([-100,100])
    axes.set_ylim([0,0.0001])
    plt.legend(bbox_to_anchor=(1, 1), loc=1, borderaxespad=0.)
    plt.savefig(path + '/'+str(i) + '.png', bbox_inches='tight')
    # red_patch = mpatches.Patch(color='red', label='The red data')
    # plt.legend(handles=[red_patch])
    # axes.set_ylim([ymin,ymax])
    # plt.show()
    plt.close()

sdvigka = -60

while sdvigka<60:
    P = 0
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

    Plot(graph_x,graph_y,sdvigka+60)
    x.append(sdvigka)
    y.append(P)
    sdvigka+=1
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
    print('!creating: ... |', path + '1' + '.gif')
    imageio.mimsave(path + '1' + '.gif', images)
    print('!done:', path + '1' + '.gif')
gif(path+'/')
