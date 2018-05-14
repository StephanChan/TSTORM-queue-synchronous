import numpy as np
from PyQt5.QtWidgets import *
import ctypes
import time
import sys

class galvoGui(QWidget):
    def __init__(self):
        super().__init__()
        self.show()


    def setupUI(self):
        self.setWindowTitle('Galvo')
        self.setGeometry(500, 500, 200, 50)
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        self.gridGroupBox = QGroupBox("Galvo",self)

        label_V=QLabel(self.gridGroupBox)
        label_V.setText('set Voltage(0-2)')
        self.textbox_V=QDoubleSpinBox(self.gridGroupBox)
        self.textbox_V.setValue(0.5)
        self.button=QPushButton('run',self)
        self.button.setCheckable(True)


        self.label_F=QLabel(self.gridGroupBox)
        self.label_F.setText('set Frequency')
        self.textbox_F=QDoubleSpinBox(self.gridGroupBox)
        self.textbox_F.setMaximum(1000)
        self.textbox_F.setValue(100)
        self.refresh=QPushButton('refresh',self)

        label_offset=QLabel('offset',self.gridGroupBox)
        self.offset=QDoubleSpinBox(self.gridGroupBox)
        self.offset.setMinimum(-1)
        self.offset.setValue(0)

        
        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label_V, 1, 0)
        layout.addWidget(self.textbox_V, 1, 1)
        layout.addWidget(self.button,1,2)
        layout.addWidget(self.label_F, 2, 0)
        layout.addWidget(self.textbox_F, 2, 1)
        layout.addWidget(self.refresh,2,2)
        layout.addWidget(self.offset,3,1)
        layout.addWidget(label_offset,3,0)


        layout.setColumnStretch(1, 1)
        self.gridGroupBox.setLayout(layout)
        mainLayout.addWidget(self.gridGroupBox)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GalvoGui()
    sys.exit(app.exec_())