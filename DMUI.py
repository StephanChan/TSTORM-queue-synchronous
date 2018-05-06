from PyQt5 import QtWidgets,QtGui,QtCore

class dmUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        #self.setup()
        #self.show()

    def setup(self):
        self.setWindowTitle('DM control')
        self.setGeometry(100, 100, 200, 200)
        mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(mainLayout)
        horizontalLayout_1=QtWidgets.QHBoxLayout()
        self.on_button=QtWidgets.QPushButton('init DM',self)
        self.on_button.setCheckable(True)
        self.aberration_button=QtWidgets.QPushButton('remove aberration',self)
        horizontalLayout_1.addWidget(self.on_button)
        horizontalLayout_1.addWidget(self.aberration_button)

        horizontalLayout_2=QtWidgets.QHBoxLayout()
        label=QtWidgets.QLabel('astigmatism<1',self)
        self.textbox=QtWidgets.QLineEdit(self)
        self.textbox.setText('0')
        self.astig_button=QtWidgets.QPushButton('set',self)
        horizontalLayout_2.addWidget(label)
        horizontalLayout_2.addWidget(self.textbox)
        horizontalLayout_2.addWidget(self.astig_button)

        mainLayout.addLayout(horizontalLayout_1)
        mainLayout.addLayout(horizontalLayout_2)


if __name__=='__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ex = dmUI()
    sys.exit(app.exec_())
