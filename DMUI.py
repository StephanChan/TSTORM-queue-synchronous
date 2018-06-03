from PyQt5 import QtWidgets,QtGui,QtCore
import gene_zernike_mode as modes

class dmUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup()
        self.show()

    def setup(self):
        self.setWindowTitle('DM control')
        self.setGeometry(100, 100, 400, 400)
        mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(mainLayout)
        horizontalLayout_1=QtWidgets.QHBoxLayout()
        self.on_button=QtWidgets.QPushButton('init DM',self)
        self.on_button.setCheckable(True)
        self.aberration_button=QtWidgets.QPushButton('remove aberration',self)
        horizontalLayout_1.addWidget(self.on_button)
        horizontalLayout_1.addWidget(self.aberration_button)
        mainLayout.addLayout(horizontalLayout_1)


        for i,item in enumerate(modes.modes):

            globals()['horizontalLayout_'+str(i)]=QtWidgets.QHBoxLayout()
            globals()['label_'+str(i)]=QtWidgets.QLabel(item,self)
            globals()['self.textbox_'+str(i)]=QtWidgets.QLineEdit(self)
            globals()['self.textbox_' + str(i)].setText('0')
            globals()['self.button_'+str(i)]=QtWidgets.QPushButton('set',self)
            globals()['horizontalLayout_' + str(i)].addWidget(globals()['label_'+str(i)])
            globals()['horizontalLayout_' + str(i)].addWidget(globals()['self.textbox_'+str(i)])
            globals()['horizontalLayout_' + str(i)].addWidget(globals()['self.button_'+str(i)])
            mainLayout.addLayout(globals()['horizontalLayout_'+str(i)])




if __name__=='__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ex = dmUI()
    sys.exit(app.exec_())
