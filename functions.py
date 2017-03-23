# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math, cmath
import scipy.integrate as integrate
from scipy.integrate import quad

# -----------Аппаратная функция-------------------

def sample_curve(dTeta,teta,itta,X0,Xh,tetaprmtr_deg,fi):
	tetaprmtr = math.radians(tetaprmtr_deg)
	gamma_0 = math.sin(math.radians(90-fi) + tetaprmtr)
	gamma_h = math.sin(math.radians(90-fi) - tetaprmtr)
	b=gamma_0/abs(gamma_h) # коэффициент ассиметрии брэговского отражения
	C = 1
	sample = dTeta+teta+(itta-1)*math.tan(tetaprmtr)#поменять знак плюс перед итта
	alfa = -4*math.sin(tetaprmtr)*(math.sin(tetaprmtr+sample)-math.sin(tetaprmtr)) # угловая отстройка падающего излучения от угла Брегга
	prover = (1/4/gamma_0)*(X0*(1-b)-b*alfa+cmath.sqrt(((X0*(1+b)+b*alfa)*(X0*(1+b)+b*alfa))-4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
	if prover.imag < float(0):
		eps = (1/4/gamma_0)*(X0*(1-b)-b*alfa-cmath.sqrt(((X0*(1+b)+b*alfa)*(X0*(1+b)+b*alfa))-4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
	else:
		eps = prover
	R = (2*eps*gamma_0-X0)/Xh/C
	return (gamma_h/gamma_0)*abs(R)*abs(R)


#-----------Монохроматор-----------
def monohromator_curve(teta, itta,X0,Xh,tetaprmtr_deg,fi):
	tetaprmtr = math.radians(tetaprmtr_deg)
	gamma_0 = math.sin(math.radians(90-fi) + tetaprmtr)
	gamma_h = math.sin(math.radians(90-fi) - tetaprmtr)
	b=gamma_0/abs(gamma_h) # коэффициент ассиметрии брэговского отражения
	C = 1
	monohrom = teta+(itta-1)*math.tan(tetaprmtr)#поменять знак плюс перед итта
	alfa = -4*math.sin(tetaprmtr)*(math.sin(tetaprmtr+monohrom)-math.sin(tetaprmtr)) # угловая отстройка падающего излучения от угла Брегга
	prover = (1/4/gamma_0)*(X0*(1-b)-b*alfa+cmath.sqrt(((X0*(1+b)+b*alfa)*(X0*(1+b)+b*alfa))-4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
	if prover.imag < float(0):
		eps = (1/4/gamma_0)*(X0*(1-b)-b*alfa-cmath.sqrt(((X0*(1+b)+b*alfa)*(X0*(1+b)+b*alfa))-4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
	else:
		eps = prover
	R = (2*eps*gamma_0-X0)/Xh/C
	return (gamma_h/gamma_0)*abs(R)*abs(R)

def gauss(sigma,mu,x):
	return 1/(sigma*math.sqrt(2*math.pi))*math.exp(-((x-mu)**2)/(2*sigma**2))

#-----------спектральная функция-----------
def g_lambd(itta,wavelength_1,wavelength_2):
	d_lambd1 = wavelength_1*3e-4
	d_lambd2 = wavelength_2*3e-4
	return 2/3/math.pi*((d_lambd1/wavelength_1)/(math.pow((itta-1),2)+math.pow(d_lambd1/wavelength_1,2))+0.5*(d_lambd2/wavelength_1)/(math.pow((itta-wavelength_2/wavelength_1),2)+math.pow((d_lambd2/wavelength_1),2)))

def frenel_slit(lam,phi,slit,L,I0=1):
	if abs(phi)<1:
		argument = phi
	else:
		argument = math.radians(phi/3600)
	stright_ray = math.atan(slit/2/L)
	if stright_ray>abs(argument):
		return I0
	else:
		znak = argument/abs(argument)
		argument = (abs(argument) - stright_ray)*znak
		u = math.pi*slit/lam*math.sin(argument)
		return I0*math.pow(math.sin(u)/u,2)

def sample_curve_broken(dTeta,teta,itta,X0,Xh,tetaprmtr_deg,fi,extintion,l_plenka,da_plenka,fwhm,amorphizaciya):
	wavelength = itta*0.709300*1e-10
	tetaprmtr = math.radians(tetaprmtr_deg)
	gamma_0 = math.sin(math.radians(90-fi) + tetaprmtr)
	gamma_h = math.sin(math.radians(90-fi) - tetaprmtr)
	b=gamma_0/abs(gamma_h) # коэффициент ассиметрии брэговского отражения
	C = 1
	sample = dTeta+teta-(itta-1)*math.tan(tetaprmtr)
	alfa = -4*math.sin(tetaprmtr)*(math.sin(tetaprmtr+sample)-math.sin(tetaprmtr)) # угловая отстройка падающего излучения от угла Брегга
	prover = (1/4/gamma_0)*(X0*(1-b)-b*alfa+cmath.sqrt(((X0*(1+b)+b*alfa)*(X0*(1+b)+b*alfa))-4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
	if prover.imag < float(0):
		eps = (1/4/gamma_0)*(X0*(1-b)-b*alfa-cmath.sqrt(((X0*(1+b)+b*alfa)*(X0*(1+b)+b*alfa))-4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
	else:
		eps = prover

	kh = math.sin(tetaprmtr)/wavelength
	koef_teta = fwhm/sample
	koef_l = l_plenka/extintion

	Rd = koef_teta * cmath.exp( - amorphizaciya - 1j * kh * da_plenka * l_plenka+1j*koef_l/koef_teta)*( cmath.exp( -1j * koef_l/koef_teta ) - 1 )
	R = (2*eps*gamma_0-X0)/Xh/C
	res = Rd + R
	return (gamma_h/gamma_0)*abs(res)*abs(res)


def sample_curve_broken_integrate(dTeta,teta,itta,X0,Xh,tetaprmtr_deg,fi,extintion,l_plenka,da_plenka,fwhm,amorphizaciya):
	wavelength = itta*0.709300*1e-10
	tetaprmtr = math.radians(tetaprmtr_deg)
	gamma_0 = math.sin(math.radians(90-fi) + tetaprmtr)
	gamma_h = math.sin(math.radians(90-fi) - tetaprmtr)
	b=gamma_0/abs(gamma_h) # коэффициент ассиметрии брэговского отражения
	C = 1
	sample = dTeta+teta-(itta-1)*math.tan(tetaprmtr)
	alfa = -4*math.sin(tetaprmtr)*(math.sin(tetaprmtr+sample)-math.sin(tetaprmtr)) # угловая отстройка падающего излучения от угла Брегга
	prover = (1/4/gamma_0)*(X0*(1-b)-b*alfa+cmath.sqrt(((X0*(1+b)+b*alfa)*(X0*(1+b)+b*alfa))-4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
	if prover.imag < float(0):
		eps = (1/4/gamma_0)*(X0*(1-b)-b*alfa-cmath.sqrt(((X0*(1+b)+b*alfa)*(X0*(1+b)+b*alfa))-4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
	else:
		eps = prover

	def integrand(x, da_plenka, l_plenka, amorphizaciya,fwhm,sample,extintion,tetaprmtr,wavelength):
		def uz(x,da_plenka):
			return da_plenka
		u = quad(uz, 0, l_plenka, args=(da_plenka))
		koef_teta = sample/fwhm
		kh = math.pow((math.sin(tetaprmtr)/wavelength),2)
		a = cmath.exp( -amorphizaciya + (1j*koef_teta*(l_plenka-x)/extintion) - 1j*kh*u)
		return a

	I = quad(integrand, 0, l_plenka, args=(da_plenka, l_plenka, amorphizaciya,fwhm,sample,extintion,tetaprmtr,wavelength))
	Rd = -1j/extintion*I
	R = (2*eps*gamma_0-X0)/Xh/C
	res = Rd + R
	return (gamma_h/gamma_0)*abs(res)*abs(res)
