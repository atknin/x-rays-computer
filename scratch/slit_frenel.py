import matplotlib.pyplot as plt
import math

lam = 0.709300*math.pow(10,-10)
slit = 0.3 * math.pow(10,-3)

wavelength_1 = 0.709300*math.pow(10,-10)
wavelength_2 = 0.713590*math.pow(10,-10)

def g_lambd(wavelength):
	d_lambd1 = wavelength_1*3e-4
	d_lambd2 = wavelength_2*3e-4
	return 2/3/math.pi*(d_lambd1/((wavelength-wavelength_1)*(wavelength-wavelength_1)+d_lambd1*d_lambd1)+0.5*d_lambd2/((wavelength-wavelength_2)*(wavelength-wavelength_2)+d_lambd2*d_lambd2))

def frenel_slit(lam,phi,slit,L,I0=1):
	argument = math.radians(phi/3600)
    stright_ray = math.atan(slit/2/L)
	if stright_ray>abs(argument):
        return I0
    else:
        znak = argument/abs(argument)
        argument = (abs(argument) - stright_ray)*znak
        u = math.pi*slit/lam*math.sin(argument)
        return I0*math.pow(math.sin(u)/u,2)

delta = abs(wavelength_2 - wavelength_1)
lam = wavelength_1-delta
end = wavelength_2+delta
shag = (end-lam)/1000
x_left = []
x_right = []
y_right = []
y_left = []

for i in range(1,2000/2):
    if i == 0:
        pass
    else:

        x_left.append(i/10)
        y_right.append(0)
        y_left.append(0)

while lam <= end:
    # x.append(lam)
    # y.append(g_lambd(lam))
    for i in range(-2000,0):
        if i == 0:
            pass
        else:
            y_left[i+2000-1] += frenel_slit(lam,i/10,slit)

    for i in range(1,2000):
        if i == 0:
            pass
        else:
            y_left[i-1] += frenel_slit(lam,i/10,slit)
    lam+=shag

plt.plot(x,y, 'o')
plt.plot(x,y, 'o')
# plt.ylim(70,110)
plt.show()
