import numpy as np
import math
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
actuator_x=[-3.75,-1.25,1.25,3.75,
            -6.25,-3.75,-1.25,1.25,3.75,6.25,
            -8.75,-6.25,-3.75,-1.25,1.25,3.75,6.25,8.75,
            -8.75, -6.25, -3.75, -1.25, 1.25, 3.75, 6.25, 8.75,
            -8.75, -6.25, -3.75, -1.25, 1.25, 3.75, 6.25, 8.75,
            -8.75, -6.25, -3.75, -1.25, 1.25, 3.75, 6.25, 8.75,
            -6.25, -3.75, -1.25, 1.25, 3.75, 6.25,
            -3.75, -1.25, 1.25, 3.75]
actuator_y=[8.75,8.75,8.75,8.75,
            6.25,6.25,6.25,6.25,6.25,6.25,
            3.75,3.75,3.75,3.75,3.75,3.75,3.75,3.75,
            1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,
            -1.25,-1.25,-1.25,-1.25,-1.25,-1.25,-1.25,-1.25,
            -3.75,-3.75,-3.75,-3.75,-3.75,-3.75,-3.75,-3.75,
            -6.25,-6.25,-6.25,-6.25,-6.25,-6.25,
            -8.75,-8.75,-8.75,-8.75]
#fig=plt.figure()
#ax=Axes3D(fig)
#plt.plot(actuator_x,actuator_y,'o')
#plt.show()
def astigmatism_at_0(x,y):
    l=np.sqrt(x**2+y**2)/7.5/np.sqrt(2)
    theta=math.atan(y/x)
    return np.sqrt(6)*l**2*np.cos(2*theta)

astigmatism_at_0_modes=[]
count=0
for i in range(52):
    astigmatism_at_0_modes+=[astigmatism_at_0(actuator_x[i],actuator_y[i])]
    count+=np.abs(astigmatism_at_0(actuator_x[i],actuator_y[i]))
astigmatism_at_0_modes=np.array(astigmatism_at_0_modes)/(count/25.0)

#ax.plot(actuator_x,actuator_y,astigmatism_at_0_modes,'o')
#plt.show()
def astigmatism_at_45(x,y):
    l = np.sqrt(x ** 2 + y ** 2) / 7.5 / np.sqrt(2)
    theta = math.atan(y / x)
    return np.sqrt(6) * l ** 2 * np.sin(2 * theta)

astigmatism_at_45_modes=[]
count=0
for i in range(52):
    astigmatism_at_45_modes+=[astigmatism_at_45(actuator_x[i],actuator_y[i])]
    count+=np.abs(astigmatism_at_45(actuator_x[i],actuator_y[i]))
astigmatism_at_45_modes=np.array(astigmatism_at_45_modes)/(count/25.0)

def coma_at_90(x,y):
    l = np.sqrt(x ** 2 + y ** 2) / 7.5 / np.sqrt(2)
    theta = math.atan(y / x)
    return np.sqrt(8) *( 3*l ** 3-2*l )* np.sin(theta)

coma_at_90_modes=[]
count=0
for i in range(52):
    coma_at_90_modes+=[coma_at_90(actuator_x[i],actuator_y[i])]
    count+=np.abs(coma_at_90(actuator_x[i],actuator_y[i]))
coma_at_90=np.array(coma_at_90_modes)/(count/25.0)

def coma_at_0(x,y):
    l = np.sqrt(x ** 2 + y ** 2) / 7.5 / np.sqrt(2)
    theta = math.atan(y / x)
    return np.sqrt(8) * (3 * l ** 3 - 2 * l) * np.cos(theta)

coma_at_0_modes=[]
count=0
for i in range(52):
    coma_at_0_modes+=[coma_at_0(actuator_x[i],actuator_y[i])]
    count+=np.abs(coma_at_0(actuator_x[i],actuator_y[i]))
coma_at_0=np.array(coma_at_0_modes)/(count/25.0)

def trenfoil_at_90(x,y):
    l = np.sqrt(x ** 2 + y ** 2) / 7.5 / np.sqrt(2)
    theta = math.atan(y / x)
    return np.sqrt(8) * l ** 3 * np.sin(3*theta)

trenfoil_at_90_modes=[]
count=0
for i in range(52):
    trenfoil_at_90_modes+=[trenfoil_at_90(actuator_x[i],actuator_y[i])]
    count+=np.abs(trenfoil_at_90(actuator_x[i],actuator_y[i]))
trenfoil_at_90=np.array(trenfoil_at_90_modes)/(count/25.0)

def trenfoil_at_45(x,y):
    l = np.sqrt(x ** 2 + y ** 2) / 7.5 / np.sqrt(2)
    theta = math.atan(y / x)
    return np.sqrt(8) * l ** 3 * np.cos(3 * theta)

trenfoil_at_45_modes=[]
count=0
for i in range(52):
    trenfoil_at_45_modes+=[trenfoil_at_45(actuator_x[i],actuator_y[i])]
    count+=np.abs(trenfoil_at_45(actuator_x[i],actuator_y[i]))
trenfoil_at_45=np.array(trenfoil_at_45_modes)/(count/25.0)

def spherical_abrration(x,y):
    l = np.sqrt(x ** 2 + y ** 2) / 7.5 / np.sqrt(2)
    theta = math.atan(y / x)
    return np.sqrt(5) * (6*l ** 4-6*l**2+1)

spherical_abrration_modes=[]
count=0
for i in range(52):
    spherical_abrration_modes+=[spherical_abrration(actuator_x[i],actuator_y[i])]
    count+=np.abs(spherical_abrration(actuator_x[i],actuator_y[i]))
spherical_abrration=np.array(spherical_abrration_modes)/(count/25.0)

def quadrafoil_at_90(x,y):
    l = np.sqrt(x ** 2 + y ** 2) / 7.5 / np.sqrt(2)
    theta = math.atan(y / x)
    return np.sqrt(10) * l ** 4 * np.cos(4 * theta)

quadrafoil_at_90_modes=[]
count=0
for i in range(52):
    quadrafoil_at_90_modes+=[quadrafoil_at_90(actuator_x[i],actuator_y[i])]
    count+=np.abs(quadrafoil_at_90(actuator_x[i],actuator_y[i]))
quadrafoil_at_90=np.array(quadrafoil_at_90_modes)/(count/25.0)

def quadrafoil_at_45(x,y):
    l = np.sqrt(x ** 2 + y ** 2) / 7.5 / np.sqrt(2)
    theta = math.atan(y / x)
    return np.sqrt(10) * l ** 4 * np.sin(4 * theta)

quadrafoil_at_45_modes=[]
count=0
for i in range(52):
    quadrafoil_at_45_modes+=[quadrafoil_at_45(actuator_x[i],actuator_y[i])]
    count+=np.abs(quadrafoil_at_45(actuator_x[i],actuator_y[i]))
quadrafoil_at_45=np.array(quadrafoil_at_45_modes)/(count/25.0)

modes={'astigmatism_at_0':astigmatism_at_0_modes,'astigmatism_at_45':astigmatism_at_45_modes,
       'coma_at_90':coma_at_90_modes,'coma_at_0':coma_at_0_modes,
       'trenfoil_at_90':trenfoil_at_90_modes,'trenfoil_at_45':trenfoil_at_45_modes,
       'spherical_abrration':spherical_abrration_modes,
       'quadrafoil_at_90':quadrafoil_at_90_modes,'quadrafoil_at_45':quadrafoil_at_45_modes}


