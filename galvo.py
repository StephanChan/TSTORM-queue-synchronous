import numpy as np
import module
import galvoUI as ui
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import PyDAQmx
import ctypes
import time
import sys

class Galvo(QWidget):
    def __init__(self):
        super().__init__()
        self.ui=ui.galvoGui()
        self.ui.setupUI()
        self.ui.refresh.clicked.connect(lambda: self.refresh())
        self.ui.button.clicked.connect(lambda: self.galvo())


    def galvo(self):
        if self.ui.button.isChecked():

            self.ui.button.setText('stop')
            num = float(self.ui.textbox_V.text())#range of galvo
            frequency = float(self.ui.textbox_F.text())#frequency of galvo

            self.task=PyDAQmx.Task()#init self.task
            #choose ao0 channel to export voltage to Galvo
            self.task.CreateAOVoltageChan("/Dev1/ao0", "", -2.0, 2.0,#voltage range is [-2,2]
                                     PyDAQmx.DAQmx_Val_Volts, None)
            #PyDAQmx.DAQmx_Val_ContSamps set voltage signal as infinite number and continuous
            self.task.CfgSampClkTiming("", int(frequency) * 2000, PyDAQmx.DAQmx_Val_Rising, PyDAQmx.DAQmx_Val_ContSamps, int(frequency) * 2000)
            #init voltage  data to export
            list = np.abs(num*np.arange(-2, 2, 0.002), dtype=np.float64) - num+float(self.ui.offset.text())
            list = np.tile(list, 2 * int(frequency))
            list = np.float64(list)
            #export this data
            self.task.WriteAnalogF64(int(frequency) * 2000, 0, -1, PyDAQmx.DAQmx_Val_GroupByChannel, list, None, None)
            self.task.StartTask()
        else:
            self.ui.button.setText('run')
            self.stop()



    def stop(self):
        self.task.StopTask()
        #self.task.clear()
        self.task = PyDAQmx.Task()
        self.task.CreateAOVoltageChan("/Dev1/ao0", "", -2.0, 2.0,
                                      PyDAQmx.DAQmx_Val_Volts, None)
        self.task.WriteAnalogScalarF64(1, 10.0, 0, reserved=None)

        #self.task.StopTask()

#change frequency and restart Galvo
    def refresh(self):
        try:
            self.task.StopTask()
        except:
            pass
        self.galvo()

    '''class AOTask(PyDAQmx.Task):
        """Class for managing continuous analog output with NI devices
        :param chans: Analog output channels to generate data on
        :type chans: list<str>
        :param samplerate: Sampling frequency (Hz) at which data points are generated
        :type samplerate: int
        :param bufsize: length (in samples) of the data buffer for each channel
        :type bufsize: int
        :param clksrc: source terminal for the sample clock, default is internal clock
        :type clksrc: str
        :param trigsrc: source of a digital trigger to start the generation
        :type trigsrc: str
        """
        def __init__(self, chan, samplerate, bufsize, clksrc="", trigsrc=""):
            PyDAQmx.Task.__init__(self)
            self.bufsize = bufsize
            self.chan = chan
            self.CreateAOVoltageChan(chan, "", -2.0, 2.0,
                                     PyDAQmx.DAQmx_Val_Volts, None)
            self.CfgSampClkTiming(clksrc, samplerate, PyDAQmx.DAQmx_Val_Rising,
                                  PyDAQmx.DAQmx_Val_ContSamps, bufsize)
            # starts the AO and AI at the same time
            if len(trigsrc) > 0:
                self.CfgDigEdgeStartTrig(trigsrc, PyDAQmx.DAQmx_Val_Rising)
            self.AutoRegisterDoneEvent(0)
        def start(self):
            """Begins generation -- immediately if not using a trigger"""
            self.StartTask()
        def write(self, output):
            """Writes the data to be output to the device buffer, output will be looped when the data runs out
            :param output: data to output
            :type output: numpy.ndarray
            """
            w = ctypes.c_int32()
            # print "output max", max(abs(output))
            self.WriteAnalogF64(self.bufsize, 0, 10.0, PyDAQmx.DAQmx_Val_GroupByChannel,
                                output, w, None);
        def stop(self):
            """Halts the Generation"""
            self.StopTask()
            self.WriteAnalogScalarF64(0, 10.0, -0.5, None)
            self.StartTask()
            self.StopTask()
            self.ClearTask()'''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Galvo()
    sys.exit(app.exec_())