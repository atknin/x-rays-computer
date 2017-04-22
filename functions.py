# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math
import cmath
import scipy.integrate as integrate
from scipy.integrate import quad
import operator

# -----------Аппаратная функция-------------------


def sample_curve(dTeta, teta, itta, X0, Xh, tetaprmtr_deg, fi):
    tetaprmtr = math.radians(tetaprmtr_deg)
    gamma_0 = math.sin(math.radians(fi) + tetaprmtr)
    gamma_h = math.sin(math.radians(fi) - tetaprmtr)
    # коэффициент ассиметрии брэговского отражения    # Ignore
    # SpaceConsistencyBear
    b = gamma_0/abs(gamma_h)
    C = 1
    sample = dTeta+teta-(itta-1)*math.tan(tetaprmtr)  # поменять знак плюсь
    # угловая отстройка падающего излучения от угла Брегга
    alfa = -4*math.sin(tetaprmtr) * \
        (math.sin(tetaprmtr+sample)-math.sin(tetaprmtr))
    prover = (1/4/gamma_0)*(X0*(1-b)-b*alfa+cmath.sqrt(((X0*(1+b)+b*alfa)*(X0*(1+b)+b*alfa)
                                                        )-4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
    if prover.imag < float(0):
        eps = (1/4/gamma_0)*(X0*(1-b)-b*alfa-cmath.sqrt(((X0*(1+b)+b*alfa)*(X0*(1+b)+b*alfa)
                                                         )-4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
    else:
        eps = prover
    R = (2*eps*gamma_0-X0)/Xh/C
    return (abs(gamma_h)/gamma_0)*abs(R)*abs(R)


#-----------Монохроматор-----------
def monohromator_curve(teta, itta, X0, Xh, tetaprmtr_deg, fi):
    tetaprmtr = math.radians(tetaprmtr_deg)
    gamma_0 = math.sin(math.radians(fi) + tetaprmtr)
    gamma_h = math.sin(math.radians(fi) - tetaprmtr)
    b = gamma_0/abs(gamma_h)  # коэффициент ассиметрии брэговского отражения
    C = 1
    monohrom = teta-(itta-1)*math.tan(tetaprmtr)
    # угловая отстройка падающего излучения от угла Брегга
    alfa = -4*math.sin(tetaprmtr) * \
        (math.sin(tetaprmtr+monohrom)-math.sin(tetaprmtr))
    prover = (1/4/gamma_0)*(X0*(1-b)-b*alfa+cmath.sqrt(((X0*(1+b)+b*alfa)*(X0*(1+b)+b*alfa)
                                                        )-4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
    if prover.imag < float(0):
        eps = (1/4/gamma_0)*(X0*(1-b)-b*alfa-cmath.sqrt(((X0*(1+b)+b*alfa)*(X0*(1+b)+b*alfa)
                                                         )-4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
    else:
        eps = prover
    R = (2*eps*gamma_0-X0)/Xh/C
    return (abs(gamma_h)/gamma_0)*abs(R)*abs(R)


def gauss(sigma, mu, x):
    return 1/(sigma*math.sqrt(2*math.pi))*math.exp(-((x-mu)**2)/(2*sigma**2))

# -----------Аппаратная функция Чуев-------------------
def apparatnaya(teta,teta_1,teta_2,L1x,L2x,S1,S2,sigmaX = 0.0005):
    def x1(teta):
        return -(S1/2+abs(teta)*L1x)/(math.sqrt(2)*sigmaX)

    def x2(teta):

        if teta_1 >= abs(teta):
            return (S1/2-abs(teta)*L1x)/(math.sqrt(2)*sigmaX)

        elif abs(teta)>=teta_1 and abs(teta)<=teta_2:
            return (S2/2-abs(teta)*L2x)/(math.sqrt(2)*sigmaX)

    return integrate.quad(lambda x: math.exp(-x*x) ,x1(teta),x2(teta))[0]

#-----------спектральная функция-----------
def g_lambd(itta, wavelength_1, wavelength_2):
    d_lambd1 = wavelength_1*3e-4
    d_lambd2 = wavelength_2*3e-4
    return 2/3/math.pi*((d_lambd1/wavelength_1)/(math.pow((itta-1), 2)+math.pow(d_lambd1/wavelength_1, 2))+0.5*(d_lambd2/wavelength_1)/(math.pow((itta-wavelength_2/wavelength_1), 2)+math.pow((d_lambd2/wavelength_1), 2)))


def frenel_slit(lam, phi, slit, L, I0=1):
    if abs(phi) < 1:
        argument = phi
    else:
        argument = math.radians(phi/3600)
    stright_ray = math.atan(slit/2/L)
    if stright_ray > abs(argument):
        return I0
    else:
        znak = argument/abs(argument)
        argument = (abs(argument) - stright_ray)*znak
        u = math.pi*slit/lam*math.sin(argument)
        return I0*math.pow(math.sin(u)/u, 2)

def slit_extensive_source(teta,sdvigka,L1,L2,S1,S2,sigma):
    sdvigka = math.radians(sdvigka/3600) * L2
    teta_radian = math.radians(teta/3600)

    m = [(-sigma/2),(-S1/2 - teta_radian * L1),(-S2/2 - teta_radian * L2 + sdvigka)]
    p = [(sigma/2),(S1/2 - teta_radian * L1),(S2/2 - teta_radian * L2 + sdvigka)]
    minus = max(m)
    plus = min(p)

    if minus >= plus:
        res = 0
    else:
        res = plus - minus
    return res



# Ниже две функции для образца с нарушенным слоем
def sample_curve_broken(dTeta, teta, itta, X0, Xh, tetaprmtr_deg, fi, extintion, l_plenka, da_plenka, fwhm, amorphizaciya):
    wavelength = itta*0.709300*1e-10
    tetaprmtr = math.radians(tetaprmtr_deg)
    gamma_0 = math.sin(math.radians(fi) + tetaprmtr)
    gamma_h = math.sin(math.radians(fi) - tetaprmtr)
    b = gamma_0/abs(gamma_h)  # коэффициент ассиметрии брэговского отражения
    C = 1
    sample = dTeta+teta-(itta-1)*math.tan(tetaprmtr)
    # угловая отстройка падающего излучения от угла Брегга
    alfa = -4*math.sin(tetaprmtr) * \
        (math.sin(tetaprmtr+sample)-math.sin(tetaprmtr))
    prover = (1/4/gamma_0)*(X0*(1-b)-b*alfa+cmath.sqrt(((X0*(1+b)+b*alfa)*(X0*(1+b)+b*alfa)
                                                        )-4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
    if prover.imag < float(0):
        eps = (1/4/gamma_0)*(X0*(1-b)-b*alfa-cmath.sqrt(((X0*(1+b)+b*alfa)*(X0*(1+b)+b*alfa)
                                                         )-4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
    else:
        eps = prover

    kh = math.sin(tetaprmtr)/wavelength
    koef_teta = fwhm/sample
    koef_l = l_plenka/extintion

    Rd = koef_teta * cmath.exp(- amorphizaciya - 1j * kh * da_plenka *
                               l_plenka+1j*koef_l/koef_teta)*(cmath.exp(-1j * koef_l/koef_teta) - 1)
    R = (2*eps*gamma_0-X0)/Xh/C
    res = Rd + R
    return (abs(gamma_h)/gamma_0)*abs(res)*abs(res)


def sample_curve_broken_integrate(dTeta, teta, itta, X0, Xh, tetaprmtr_deg, fi, extintion, l_plenka, da_plenka, fwhm, amorphizaciya):
    wavelength = itta*0.709300*1e-10
    tetaprmtr = math.radians(tetaprmtr_deg)
    gamma_0 = math.sin(math.radians(fi) + tetaprmtr)
    gamma_h = math.sin(math.radians(fi) - tetaprmtr)
    b = gamma_0/abs(gamma_h)  # коэффициент ассиметрии брэговского отражения
    C = 1
    sample = dTeta+teta-(itta-1)*math.tan(tetaprmtr)
    # угловая отстройка падающего излучения от угла Брегга
    alfa = -4*math.sin(tetaprmtr) * \
        (math.sin(tetaprmtr+sample)-math.sin(tetaprmtr))
    prover = (1/4/gamma_0)*(X0*(1-b)-b*alfa+cmath.sqrt(((X0*(1+b)+b*alfa)*(X0*(1+b)+b*alfa)
                                                        )-4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
    if prover.imag < float(0):
        eps = (1/4/gamma_0)*(X0*(1-b)-b*alfa-cmath.sqrt(((X0*(1+b)+b*alfa)*(X0*(1+b)+b*alfa)
                                                         )-4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
    else:
        eps = prover

    def integrand(x, da_plenka, l_plenka, amorphizaciya, fwhm, sample, extintion, tetaprmtr, wavelength):
        def uz(x, da_plenka):
            return da_plenka
        u = quad(uz, 0, l_plenka, args=(da_plenka))
        koef_teta = sample/fwhm
        kh = math.pow((math.sin(tetaprmtr)/wavelength), 2)
        a = cmath.exp(-amorphizaciya + (1j*koef_teta *
                                        (l_plenka-x)/extintion) - 1j*kh*u)
        return a

    I = quad(integrand, 0, l_plenka, args=(da_plenka, l_plenka,
                                           amorphizaciya, fwhm, sample, extintion, tetaprmtr, wavelength))
    Rd = -1j/extintion*I
    R = (2*eps*gamma_0-X0)/Xh/C
    res = Rd + R
    return (abs(gamma_h)/gamma_0)*abs(res)*abs(res)


def gif(path_gif):
    filenam = os.listdir(path_gif)
    filenames_a = sorted(filenam)
    filenames = filter(lambda x: x.endswith('.png'), filenames_a)
    images = []
    i = 0
    for filename in filenames:
        print(path_gif+'/'+str(i)+'.png')
        images.append(imageio.imread(path_gif+'/'+str(i)+'.png'))
        i += 1
    nme_file = path_gif.split("/")[-1]
    print('!creating: ... |', path_gif +'_'+ nme_file + '.gif')
    imageio.mimsave(path_gif +'_'+ nme_file + '.gif', images)
    print('!done:', path_gif +'_'+ nme_file + '.gif')
