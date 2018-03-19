from PyDAQmx import *
import module
from PyQt5 import QtWidgets
import shutterUI as ui
import numpy as np

class Shutter(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.gui=ui.shutterGui()
        self.gui.setupUI()
        self.gui.button_state.clicked.connect(lambda: self.shutter())
        self.gui.button_I.clicked.connect(lambda: self.intensity())
        self.task = Task()
        self.task.CreateDOChan("/Dev1/port1/line1", "", DAQmx_Val_ChanForAllLines)
        self.task.StartTask()

        self.task1 = Task()
        self.task1.CreateAOVoltageChan("/Dev1/ao1", "", minVal=0, maxVal=2, units=DAQmx_Val_Volts,
                                 customScaleName=None)
        self.task1.StartTask()

    def shutter(self):

        if self.gui.button_state.isChecked():
            self.gui.button_state.setText('ON')
            data = np.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=np.uint8)
            #self.task.WriteDigitalU8(1, 10.0, 1, None)
            self.task.WriteDigitalLines(1, 1, 10.0, DAQmx_Val_GroupByChannel, data, None, None)
            self.task.StopTask()
        else:
            self.gui.button_state.setText('OFF')
            data = np.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=np.uint8)
            #self.task.WriteDigitalU8(1, 10.0, 0, None)
            self.task.WriteDigitalLines(1, 1, 10.0, DAQmx_Val_GroupByChannel, data, None, None)
            self.task.StopTask()

    def intensity(self):

        self.task1.WriteAnalogScalarF64(1, 10.0, float((self.gui.textbox.text())), reserved=None)
        self.task1.StopTask()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Shutter()
    sys.exit(app.exec_())