# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math, cmath
# -----------Аппаратная функция-------------------

def sample_curve(dTeta,teta,itta,X0,Xh,tetaprmtr_deg,fi):
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
	R = (2*eps*gamma_0-X0)/Xh/C
	return (gamma_h/gamma_0)*abs(R)*abs(R)


#-----------Монохроматор-----------
def monohromator_curve(teta, itta,X0,Xh,tetaprmtr_deg,fi):
	tetaprmtr = math.radians(tetaprmtr_deg)
	gamma_0 = math.sin(math.radians(90-fi) + tetaprmtr)
	gamma_h = math.sin(math.radians(90-fi) - tetaprmtr)
	b=gamma_0/abs(gamma_h) # коэффициент ассиметрии брэговского отражения
	C = 1
	monohrom = teta-(itta-1)*math.tan(tetaprmtr)
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
