import gene_zernike_mode as modes
import my_diformable_mirror as dm
from scipy.optimize import leastsq
import numpy as np

def func(x,parameter):
    a,b,c=parameter
    return a*(x-b)**2+c

def residuals(parameter,y,x):
    return y-func(x,parameter)

class remove_abrration(object):
    def __init__(self):
        super().__init__()
        self.scope=[[-0.9,-0.3,0.3,0.9],
                    [-0.3,0,0.3],
                    [-0.1,-0.07,-0.03,0,0.03,0.07,0.1]]

        self.dm=dm.DMirror('dll_path')
        self.dm.mro_open()
        for mode in modes.modes.keys():
            self.one_mode_fit(mode)
        self.dm.mro_close()


    def merit_func(self,coef):
        return coef#difine merit function here

    def one_fit(self,offset,scope,mode):
        merit_value=[]
        for coef in np.array(scope)+offset:
            self.dm.mro_applySmoothCommand(mode*coef)
            merit_value+=[self.merit_func(coef)]
        p0 = [1,0,0]
        plsq = leastsq(residuals, p0, args=(merit_value, scope))
        return plsq[0][1],plsq[0][2]

    def one_mode_fit(self,mode_name):
        offset=0
        for scope in self.scope:
            offset,merit_value=self.one_fit(offset,scope,modes.modes[mode_name])
        self.dm.mro_applySmoothCommand(modes.modes[mode_name] * offset)
        print(mode_name,' ',offset)
