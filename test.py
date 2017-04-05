from functions import sample_curve
from functions import sample_curve_broken
from functions import sample_curve_broken_integrate
from functions import slit_extensive_source
import math
import cmath
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import numpy as np
a = [1, 2]
b = a
a = []
print(a)

a = [1, 2]
b = a
del a[:], b[:]
print(a, b)

dTeta = 0

teta_start = teta = -40
teta_end = 40
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
S1 = 0.1*1e-3
S2 = 0.1*1e-3
sigma = 0.19*1e-3
sdvigka = 10
while teta <= teta_end:
    teta_radians = math.radians(teta/3600)
    # Pnorm = sample_curve(dTeta, teta_radians, itta, X0, Xh, tetaprmtr_deg, fi)
    # ynorm.append(Pnorm)
    P = slit_extensive_source(teta,sdvigka,L1,L2,S1,S2,sigma)
    x.append(teta)
    y.append(P)
    teta += teta_shag
    # print(P)

plt.plot(x, y)
# plt.plot(x, ynorm)
plt.show()
