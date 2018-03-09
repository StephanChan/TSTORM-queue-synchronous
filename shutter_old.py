import PyDAQmx
from PyQt5.QtWidgets import *

from PyDAQmx import Task
import sys


class shutterGui(QWidget):
    def __init__(self):
        super().__init__()
        self.initgui()
        self.setWindowTitle('Two Photon Shutter')
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        mainLayout.addWidget(self.gridGroupBox)
        self.setGeometry(500, 500, 200, 50)
        self.show()

    def initgui(self):
        self.gridGroupBox = QGroupBox("shutter control")

        self.button_s = QPushButton('shutter state', self)
        self.button_s.setCheckable(True)
        self.button_s.clicked.connect(lambda: self.shutter())

        self.label = QLabel()
        self.label.setText(str(0))

        self.label_state = QLabel()
        self.label_state.setText('OFF')
        self.range_label=QLabel()
        self.range_label.setText('0-2V')
        self.textbox = QLineEdit(self)
        button_I=QPushButton('OK',self)
        button_I.clicked.connect(lambda: self.intensity())


        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(self.button_s, 1, 1)
        layout.addWidget(self.label_state,1,2)
        layout.addWidget(self.range_label,2,0)
        layout.addWidget(self.label,2,3)
        layout.addWidget(self.textbox, 2, 1)
        layout.addWidget(button_I,2,2)
        layout.setColumnStretch(1, 1)
        self.gridGroupBox.setLayout(layout)

    def shutter(self):

            task = Task()
            task.CreateDOChan("/Dev1/port1/line1", "", PyDAQmx.DAQmx_Val_ChanForAllLines)
            task.StartTask()
            if self.button_s.isChecked():
                self.label_state.setText('ON')
                task.WriteDigitalScalarU32(1, 10.0, 1, None)
                task.StopTask()
                #print(1)
            else:
                self.label_state.setText('OFF')
                task.WriteDigitalScalarU32(1, 10.0, 0, None)
                task.StopTask()
                #print(0)


    def intensity(self):


            self.label.setText(str(self.textbox.text()))
            task = Task()
            task.CreateAOVoltageChan("/Dev1/ao1", "", minVal=0, maxVal=2, units=PyDAQmx.DAQmx_Val_Volts, customScaleName=None)
            task.StartTask()
            task.WriteAnalogScalarF64(1,10.0,float((self.textbox.text())),reserved=None)

            #task.StopTask()
            #print(self.textbox.text())

if __name__=='__main__':
    app=QApplication(sys.argv)
    exa=shutterGui()
    sys.exit(app.exec_())