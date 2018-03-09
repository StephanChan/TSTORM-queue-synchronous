from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import sys

class shutterGui(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.show()

    def setupUI(self):
        mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(mainLayout)
        self.setGeometry(500, 500, 200, 50)
        self.setWindowTitle("shutter")
        self.gridGroupBox = QGroupBox("shutter control",self)
        label=QLabel('shutter state',self)
        self.button_state = QPushButton('ON', self.gridGroupBox)
        self.button_state.setCheckable(True)

        self.range_label=QLabel(self.gridGroupBox)
        self.range_label.setText('set Intensity(0-2V)')
        self.textbox = QLineEdit(self.gridGroupBox)
        self.button_I=QPushButton('OK',self.gridGroupBox)

        layout = QGridLayout(self)
        layout.setSpacing(10)
        layout.addWidget(label, 1, 0)
        layout.addWidget(self.button_state, 1, 1)
        layout.addWidget(self.range_label,2,0)
        layout.addWidget(self.textbox, 2, 1)
        layout.addWidget(self.button_I,2,2)
        layout.setColumnStretch(1, 1)
        self.gridGroupBox.setLayout(layout)

        mainLayout.addWidget(self.gridGroupBox)



if __name__=='__main__':
    app=QApplication(sys.argv)
    exa=shutterGui()
    sys.exit(app.exec_())