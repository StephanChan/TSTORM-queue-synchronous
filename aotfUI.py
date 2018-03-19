from PyQt5.QtWidgets import *
import PyQt5.QtWidgets as QtWidgets
import sys

class aotfGui(QWidget):
    def __init__(self):
        super().__init__()
#        self.setupUI()
        #self.show()

    def setupUI(self):
        self.setWindowTitle('AOTF control')
        self.setGeometry(400, 400, 400, 400)
        mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(mainLayout)
        self.gridGroupBox = QtWidgets.QGroupBox("AOTF control",self)
        label_1=QtWidgets.QLabel("channel 1")
        label_2 = QtWidgets.QLabel("channel 2")
        label_3 = QtWidgets.QLabel("channel 3")
        label_4 = QtWidgets.QLabel("channel 4")
        label_5 = QtWidgets.QLabel("channel 5")
        label_6 = QtWidgets.QLabel("channel 6")
        label_7 = QtWidgets.QLabel("channel 7")
        label_8 = QtWidgets.QLabel("channel 8")

        label_F=QtWidgets.QLabel("set Frequency")
        label_A = QtWidgets.QLabel("set Amplitude")

        self.textbox_f1 = QLineEdit(self)
        self.textbox_f1.setText('77.5')
        self.textbox_f2 = QLineEdit(self)
        self.textbox_f2.setText('153.205')
        self.textbox_f3 = QLineEdit(self)
        self.textbox_f4 = QLineEdit(self)
        self.textbox_f5 = QLineEdit(self)
        self.textbox_f6 = QLineEdit(self)
        self.textbox_f7 = QLineEdit(self)
        self.textbox_f8 = QLineEdit(self)

        self.button_run1=QPushButton('run',self)
        self.button_run2 = QPushButton('run', self)
        self.button_run3 = QPushButton('run', self)
        self.button_run4 = QPushButton('run', self)
        self.button_run5 = QPushButton('run', self)
        self.button_run6 = QPushButton('run', self)
        self.button_run7 = QPushButton('run', self)
        self.button_run8 = QPushButton('run', self)

        self.button_run1.setCheckable(True)
        self.button_run2.setCheckable(True)
        self.button_run3.setCheckable(True)
        self.button_run4.setCheckable(True)
        self.button_run5.setCheckable(True)
        self.button_run6.setCheckable(True)
        self.button_run7.setCheckable(True)
        self.button_run8.setCheckable(True)

        self.button_analog=QPushButton('internal',self)
        self.button_analog.setCheckable(True)

        self.textbox_a1 = QLineEdit(self)
        self.textbox_a1.setText('0.1')
        self.textbox_a2 = QLineEdit(self)
        self.textbox_a2.setText('0.1')
        self.textbox_a3 = QLineEdit(self)
        self.textbox_a4 = QLineEdit(self)
        self.textbox_a5 = QLineEdit(self)
        self.textbox_a6 = QLineEdit(self)
        self.textbox_a7 = QLineEdit(self)
        self.textbox_a8 = QLineEdit(self)


        layout = QtWidgets.QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(label_1,2,0)
        layout.addWidget(label_2, 3, 0)
        layout.addWidget(label_3, 4, 0)
        layout.addWidget(label_4, 5, 0)
        layout.addWidget(label_5, 6, 0)
        layout.addWidget(label_6, 7, 0)
        layout.addWidget(label_7, 8, 0)
        layout.addWidget(label_8, 9, 0)

        layout.addWidget(label_F, 1, 1)
        layout.addWidget(label_A, 1,2)

        layout.addWidget(self.textbox_f1, 2, 1)
        layout.addWidget(self.textbox_f2, 3, 1)
        layout.addWidget(self.textbox_f3, 4, 1)
        layout.addWidget(self.textbox_f4, 5, 1)
        layout.addWidget(self.textbox_f5, 6, 1)
        layout.addWidget(self.textbox_f6, 7, 1)
        layout.addWidget(self.textbox_f7, 8, 1)
        layout.addWidget(self.textbox_f8, 9, 1)

        layout.addWidget(self.button_run1, 2, 3)
        layout.addWidget(self.button_run2, 3,3 )
        layout.addWidget(self.button_run3, 4,3)
        layout.addWidget(self.button_run4, 5, 3)
        layout.addWidget(self.button_run5, 6, 3)
        layout.addWidget(self.button_run6, 7, 3)
        layout.addWidget(self.button_run7, 8, 3)
        layout.addWidget(self.button_run8, 9, 3)


        layout.addWidget(self.textbox_a1,2,2)
        layout.addWidget(self.textbox_a2, 3, 2)
        layout.addWidget(self.textbox_a3, 4, 2)
        layout.addWidget(self.textbox_a4, 5, 2)
        layout.addWidget(self.textbox_a5, 6, 2)
        layout.addWidget(self.textbox_a6, 7, 2)
        layout.addWidget(self.textbox_a7, 8, 2)
        layout.addWidget(self.textbox_a8, 9, 2)

        layout.addWidget(self.button_analog,1,3)
        layout.setColumnStretch(1, 1)
        self.gridGroupBox.setLayout(layout)
        mainLayout.addWidget(self.gridGroupBox)

if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    ex=aotfGui()
    sys.exit(app.exec_())