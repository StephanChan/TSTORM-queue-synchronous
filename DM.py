import gene_zernike_modes as modes
import my_difformable_mirror as dm
from scipy.optimize import leastsq
import numpy as np
import calc_merit_func_c as merit_func
import time
import threading
import DMUI as ui

def func(x,parameter):
    a,b,c=parameter
    return a*(x-b)**2+c

def residuals(parameter,y,x):
    return y-func(x,parameter)

class remove_aberration():
    def __init__(self):
        super().__init__()
        self.ui=ui.dmUI()
        self.ui.setup()
        self.ui.show()
        self.event=threading.Event()
        self.event.clear()
        self.image=None
        self.scope=[
                    [-0.1,-0.07,-0.03,0,0.03,0.07,0.1],]

        self.dm=dm.DMirror('D:\CD_MIRAO.2013.12.09-x64\dll\\x64\\mirao52e.dll')
        self.merit_func=merit_func.merit_func()
        self.ui.on_button.clicked.connect(lambda: self.open())
        self.ui.aberration_button.clicked.connect(lambda: self.aberration())
        self.ui.astig_button.clicked.connect(lambda: self.astigmatism())
        self.ui.flat_button.clicked.connect(lambda:self.flat_mode())

    def open(self):
        if self.ui.on_button.isChecked():
            self.dm.DM_open()
            self.ui.on_button.setText('close')
            aberration_thread = threading.Thread(target=self.aberration_remove, args=(self.event,), name='aberration thread')
            aberration_thread.start()
        else:
            self.dm.DM_close()
            self.ui.on_button.setText('open')

    def flat_mode(self):
        command=np.zeros((52,))
        self.dm.DM_read_file(path=b'D:\haso\\52\\flat\\FLAT_MIRAO_0271_01.mro',command=command)
        print(command)
        self.dm.DM_applySmoothCommand(command)


    def image_update(self,image):
        self.image=image[768:1280,512:1536]

    def merit_function(self,coef=None):

        return self.merit_func.calc(self.image)#difine merit function here

    def one_fit(self,offset,scope,mode,mode_name):
        merit_value = []
        for coef in np.array(scope) + offset:
            if -0.7<coef<0.7:
                print(coef)
                self.dm.DM_applySmoothCommand(np.array(mode) * coef)
                merit_value += [self.merit_function(coef=coef)]
                time.sleep(0.15)
            else:
                print(mode_name,' remove fail')
                return -2.0, 0.0

        p0 = [1, 1, 1]
        plsq = leastsq(residuals, p0, args=(merit_value, np.array(scope) + offset))
        print(merit_value,  plsq[0])
        return plsq[0][1], plsq[0][2]

    def one_mode_fit(self,mode_name):
        offset = 0
        for scope in self.scope:
            if offset>-0.7 or offset <0.7:
                offset, merit_value = self.one_fit(offset, scope, modes.modes[mode_name],mode_name)

            else:
                #print(mode_name, 'fail')
                return 0
        if offset<=-0.7 or offset >=0.7:
            return offset
        else:
            print(offset)
            self.dm.DM_applySmoothCommand(np.array(modes.modes[mode_name]) * offset)
            print(mode_name, ' ', offset)


    def aberration_remove(self,event):
        while(self.ui.on_button.isChecked()):
            event.wait()  #FIXME: how to exit properly
            event.clear()
            for mode in modes.modes.keys():
                self.one_mode_fit(mode)
                #time.sleep(0.5)


    def aberration(self):
        self.event.set()

    def astigmatism(self):
        coef=float(self.ui.textbox.text())
        self.dm.DM_applySmoothCommand(np.array(modes.modes['astigmatism_at_0'])*coef)

    def close(self):
        self.dm.mro_close()

if __name__=='__main__':
    import sys
    from PyQt5 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)
    ex = remove_aberration()
    sys.exit(app.exec_())