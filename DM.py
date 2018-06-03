import gene_zernike_mode as modes
import my_diformable_mirror as dm
from scipy.optimize import leastsq
import numpy as np
import calc_merit_func as merit_func
import time
import threading
import DMUI as ui

def func(x,parameter):
    a,b,c=parameter
    return a*(x-b)**2+c

def residuals(parameter,y,x):
    return y-func(x,parameter)

class remove_abrration():
    def __init__(self):
        super().__init__()
        self.ui=ui.dmUI()
        self.ui.setup()
        self.ui.show()
        self.event=threading.Event()
        self.scope=[[-0.9,-0.3,0.3,0.9],
                    [-0.3,0,0.3],
                    [-0.1,-0.07,-0.03,0,0.03,0.07,0.1]]

        self.dm=dm.DMirror('dll_path')
        self.merit_func=merit_func()
        self.ui.on_button.clicked.connect(lambda: self.open())
        self.ui.aberration_button.clicked.connect(lambda: self.aberration())
        self.ui.button_0.clicked.connect(lambda: self.astigmatism_at_0())
        self.ui.button_1.clicked.connect(lambda: self.astigmatism_at_45())
        self.ui.button_2.clicked.connect(lambda: self.coma_at_90())
        self.ui.button_3.clicked.connect(lambda: self.coma_at_0())
        self.ui.button_4.clicked.connect(lambda: self.trenfoil_at_90())
        self.ui.button_5.clicked.connect(lambda: self.trenfoil_at_45())
        self.ui.button_6.clicked.connect(lambda: self.spherical_abrration())
        self.ui.button_7.clicked.connect(lambda: self.quadrafoil_at_90())
        self.ui.button_8.clicked.connect(lambda: self.quadrafoil_at_45())

    def open(self):
        if self.ui.on_button.isChecked():
            self.dm.mro_open()
            self.ui.on_button.setText('close')
            aberration_thread = threading.Thread(target=self.aberration_remove(), name='aberration thread')
            aberration_thread.start()
        else:
            self.dm.mro_close()
            self.ui.on_button.setText('open')


    def image_update(self,image):
        self.image=image

    def merit_func(self):
        return self.merit_func.calc(self.image)#difine merit function here

    def one_fit(self,offset,scope,mode):
        merit_value=[]
        for coef in np.array(scope)+offset:
            self.dm.mro_applySmoothCommand(mode*coef)
            merit_value+=[self.merit_func()]
        p0 = [-1,1,1]
        plsq = leastsq(residuals, p0, args=(merit_value, scope))
        return plsq[0][1],plsq[0][2]

    def one_mode_fit(self,mode_name):
        offset=0
        for scope in self.scope:
            offset,merit_value=self.one_fit(offset,scope,modes.modes[mode_name])
        self.dm.mro_applySmoothCommand(modes.modes[mode_name] * offset)
        blank=getattr(self.ui, mode_name)
        blank.setText(str(offset))
        print(mode_name,' ',offset)


    def aberration_remove(self,event):
        while(self.ui.on_button.isChecked()):
            event.wait()  #FIXME: how to exit properly
            event.clear()
            for mode in modes.modes.keys():
                self.one_mode_fit(mode)
                time.sleep(0.5)


    def aberration(self):
        self.event.set()

    def astigmatism_at_0(self):
        coef=float(self.ui.textbox_0.text())
        self.dm.mro_applySmoothCommand(modes.modes['astigmatism_at_0']*coef)

    def astigmatism_at_45(self):
        coef=float(self.ui.textbox_1.text())
        self.dm.mro_applySmoothCommand(modes.modes['astigmatism_at_45']*coef)

    def coma_at_90(self):
        coef=float(self.ui.textbox_2.text())
        self.dm.mro_applySmoothCommand(modes.modes['coma_at_90']*coef)

    def coma_at_0(self):
        coef=float(self.ui.textbox_3.text())
        self.dm.mro_applySmoothCommand(modes.modes['coma_at_0']*coef)

    def trenfoil_at_90(self):
        coef=float(self.ui.textbox_4.text())
        self.dm.mro_applySmoothCommand(modes.modes['trenfoil_at_90']*coef)

    def trenfoil_at_45(self):
        coef=float(self.ui.textbox_5.text())
        self.dm.mro_applySmoothCommand(modes.modes['trenfoil_at_45']*coef)

    def spherical_abrration(self):
        coef=float(self.ui.textbox_6.text())
        self.dm.mro_applySmoothCommand(modes.modes['spherical_abrration']*coef)

    def quadrafoil_at_90(self):
        coef=float(self.ui.textbox_7.text())
        self.dm.mro_applySmoothCommand(modes.modes['quadrafoil_at_90']*coef)

    def quadrafoil_at_45(self):
        coef=float(self.ui.textbox_8.text())
        self.dm.mro_applySmoothCommand(modes.modes['quadrafoil_at_45']*coef)

    def close(self):
        self.dm.mro_close()