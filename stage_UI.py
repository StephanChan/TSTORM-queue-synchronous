from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os

class stageUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        #self.setupUI()
        #self.show()
        self.path=os.path.dirname(__file__)

    def setupUI(self):
        self.setWindowTitle('stage')
        self.setGeometry(400, 400, 500, 500)
        self.setMinimumSize(QtCore.QSize(100, 100))
        self.setMaximumSize(QtCore.QSize(10000, 10000))
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")



        spacerItem = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        spacerItem1=QtWidgets.QSpacerItem(100, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
# z movebutton
        self.zGroupBox = QtWidgets.QGroupBox("z axis control",self)
        self.zGroupBox.setMinimumSize(QtCore.QSize(100, 120))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.zGroupBox)
        self.verticalLayout.setSpacing(0)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.zGroupBox)
        self.zupButton = QtWidgets.QPushButton(self.zGroupBox)
        self.zupButton.setIcon(
            QtGui.QIcon("D:\storm-control-python3_pyqt5\storm-control-python3_pyqt5\storm_control\hal4000\icons\\1uparrow-128.png"))
        self.zupButton.setIconSize(QtCore.QSize(40, 40))
        self.horizontalLayout.addWidget(self.zupButton)
        self.horizontalLayout.addItem(spacerItem)

        self.zupLButton = QtWidgets.QPushButton(self.zGroupBox)
        self.zupLButton.setIcon(
            QtGui.QIcon("D:\storm-control-python3_pyqt5\storm-control-python3_pyqt5\storm_control\hal4000\icons\\2uparrow-128.png"))
        self.zupLButton.setIconSize(QtCore.QSize(40, 40))
        self.horizontalLayout.addWidget(self.zupLButton)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.zGroupBox)
        self.zdownButton = QtWidgets.QPushButton(self.zGroupBox)
        self.zdownButton.setIcon(
            QtGui.QIcon("D:\storm-control-python3_pyqt5\storm-control-python3_pyqt5\storm_control\hal4000\icons\\1downarrow1-128.png"))
        self.zdownButton.setIconSize(QtCore.QSize(40, 40))
        self.horizontalLayout_2.addWidget(self.zdownButton)
        self.horizontalLayout_2.addItem(spacerItem)

        self.zdownLButton = QtWidgets.QPushButton(self.zGroupBox)
        self.zdownLButton.setIcon(
            QtGui.QIcon("D:\storm-control-python3_pyqt5\storm-control-python3_pyqt5\storm_control\hal4000\icons\\2dowarrow-128.png"))
        self.zdownLButton.setIconSize(QtCore.QSize(40, 40))
        self.horizontalLayout_2.addWidget(self.zdownLButton)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        horizontalLayout=QtWidgets.QHBoxLayout()
        label=QtWidgets.QLabel('small move step',self.zGroupBox)
        self.small_step=QtWidgets.QDoubleSpinBox(self.zGroupBox)
        self.small_step.setDecimals(4)
        self.small_step.setMinimum(0)
        self.small_step.setMaximum(1)
        self.small_step.setValue(0.01)
        horizontalLayout.addWidget(label)
        horizontalLayout.addWidget(self.small_step)
        self.verticalLayout.addLayout(horizontalLayout)

        horizontalLayout2=QtWidgets.QHBoxLayout()
        label2=QtWidgets.QLabel('big move step',self.zGroupBox)
        self.big_step = QtWidgets.QDoubleSpinBox(self.zGroupBox)
        self.big_step.setDecimals(4)
        self.big_step.setMinimum(0)
        self.big_step.setMaximum(1)
        self.big_step.setValue(0.05)
        horizontalLayout2.addWidget(label2)
        horizontalLayout2.addWidget(self.big_step)
        self.verticalLayout.addLayout(horizontalLayout2)


        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addWidget(self.zGroupBox, 0, 0, 1, 1)

        # gridlayout--verticallayout_5--upbuttons
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self)
        self.upLButton = QtWidgets.QPushButton(self)
        self.upLButton.setIcon(QtGui.QIcon("D:\storm-control-python3_pyqt5\storm-control-python3_pyqt5\storm_control\hal4000\icons\\2uparrow-128.png"))
        self.upLButton.setIconSize(QtCore.QSize(56, 56))
        self.verticalLayout_5.addWidget(self.upLButton)
        self.upSButton = QtWidgets.QPushButton(self)
        self.upSButton.setIcon(
            QtGui.QIcon("D:\storm-control-python3_pyqt5\storm-control-python3_pyqt5\storm_control\hal4000\icons\\1uparrow-128.png"))
        self.upSButton.setIconSize(QtCore.QSize(56, 56))
        self.verticalLayout_5.addWidget(self.upSButton)
        self.gridLayout.addLayout(self.verticalLayout_5, 0, 1, 1, 1)

        # gridlayout--(posgroupbox)verticallayout_2--horizontallayout_3+horizontallayout_4+horizontallayout_5
        self.posGroupBox = QtWidgets.QGroupBox("position",self)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.posGroupBox)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self)
        self.xposLabel = QtWidgets.QLabel('x posi: 1,26 ', self.posGroupBox)
        self.horizontalLayout_3.addWidget(self.xposLabel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.yposLabel = QtWidgets.QLabel('y posi:  ', self.posGroupBox)
        self.horizontalLayout_4.addWidget(self.yposLabel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.zposLabel = QtWidgets.QLabel('z posi:  ', self.posGroupBox)
        self.horizontalLayout_14.addWidget(self.zposLabel)
        #self.zposText = QtWidgets.QLabel(self.posGroupBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_14)
        self.verticalLayout_2.addItem(spacerItem)

        self.horizontalLayout_range1 = QtWidgets.QHBoxLayout()
        self.xrangeLabel = QtWidgets.QLabel('x range:  ', self.posGroupBox)
        self.horizontalLayout_range1.addWidget(self.xrangeLabel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_range1)

        self.horizontalLayout_range2 = QtWidgets.QHBoxLayout()
        self.yrangeLabel = QtWidgets.QLabel('y range:  ', self.posGroupBox)
        self.horizontalLayout_range2.addWidget(self.yrangeLabel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_range2)

        self.horizontalLayout_range3 = QtWidgets.QHBoxLayout()
        self.zrangeLabel = QtWidgets.QLabel('z range:  ', self.posGroupBox)
        self.horizontalLayout_range3.addWidget(self.zrangeLabel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_range3)
        self.verticalLayout_2.addItem(spacerItem)
        self.posGroupBox.setLayout(self.verticalLayout_2)
        self.gridLayout.addWidget(self.posGroupBox, 0, 2, 1, 1)

# gridlayout--horizontallayout_6--leftbuttons
        #             homebutton
        #            horizontallayout_7--rightbuttons
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.xlabel=QtWidgets.QLabel('X axis',self)
        self.horizontalLayout_6.addWidget(self.xlabel)
        self.leftLButton = QtWidgets.QPushButton(self)
        self.leftLButton.setMinimumSize(QtCore.QSize(68, 66))
        self.leftLButton.setIcon(
            QtGui.QIcon("D:\storm-control-python3_pyqt5\storm-control-python3_pyqt5\storm_control\hal4000\icons\\2leftarrow-128.png"))
        self.leftLButton.setIconSize(QtCore.QSize(56, 56))
        self.horizontalLayout_6.addWidget(self.leftLButton)

        self.leftSButton = QtWidgets.QPushButton(self)
        self.leftSButton.setMinimumSize(QtCore.QSize(52, 66))
        self.leftSButton.setMaximumSize(QtCore.QSize(52, 66))
        self.leftSButton.setIcon(
            QtGui.QIcon("D:\storm-control-python3_pyqt5\storm-control-python3_pyqt5\storm_control\hal4000\icons\\1leftarrow-128.png"))
        self.leftSButton.setIconSize(QtCore.QSize(56, 56))
        self.horizontalLayout_6.addWidget(self.leftSButton)
        self.gridLayout.addLayout(self.horizontalLayout_6, 1, 0, 1, 1)

        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.rightSButton = QtWidgets.QPushButton(self)
        self.rightSButton.setMinimumSize(QtCore.QSize(52, 66))
        self.rightSButton.setMaximumSize(QtCore.QSize(52, 66))
        self.rightSButton.setIcon(
            QtGui.QIcon("D:\storm-control-python3_pyqt5\storm-control-python3_pyqt5\storm_control\hal4000\icons\\1rightarrow-128.png"))
        self.rightSButton.setIconSize(QtCore.QSize(56, 56))
        self.horizontalLayout_11.addWidget(self.rightSButton)

        self.rightLButton = QtWidgets.QPushButton(self)
        self.rightLButton.setMinimumSize(QtCore.QSize(68, 66))
        self.rightLButton.setMaximumSize(QtCore.QSize(68, 66))
        self.rightLButton.setIcon(
            QtGui.QIcon("D:\storm-control-python3_pyqt5\storm-control-python3_pyqt5\storm_control\hal4000\icons\\2rightarrow-128.png"))
        self.rightLButton.setIconSize(QtCore.QSize(56, 56))
        self.horizontalLayout_11.addWidget(self.rightLButton)
        spacerItem4 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem4)

        self.exitButton = QtWidgets.QPushButton("Exit",self)
        self.exitButton.setMinimumSize(QtCore.QSize(40, 40))
        self.exitButton.setMaximumSize(QtCore.QSize(40, 40))
        self.horizontalLayout_11.addWidget(self.exitButton)
        self.gridLayout.addLayout(self.horizontalLayout_11, 1, 2, 1, 1)

# gridlayout--(movegroupbox)verticallayout_3--horizontallayout_7+horizontallayout_8+horizontallayout_9
        self.moveGroupBox = QtWidgets.QGroupBox("customize move",self)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.moveGroupBox)
        self.verticalLayout_3.addItem(spacerItem)

        self.horizontalLayout_m7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_m7.addItem(spacerItem)
        self.xmoveLabel = QtWidgets.QLabel('x', self.moveGroupBox)
        self.horizontalLayout_m7.addWidget(self.xmoveLabel)
        self.verticalLayout_3.addItem(spacerItem)
        self.xmoveDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.moveGroupBox)
        self.xmoveDoubleSpinBox.setDecimals(3)
        self.xmoveDoubleSpinBox.setMinimum(-10.0)
        self.xmoveDoubleSpinBox.setMaximum(10.0)
        self.horizontalLayout_m7.addWidget(self.xmoveDoubleSpinBox)
        self.verticalLayout_3.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_m7)  # horizontallayout_7: xmovelabel+xdoublespinbox

        self.horizontalLayout_m8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_m8.addItem(spacerItem)
        self.ymoveLabel = QtWidgets.QLabel('y', self.moveGroupBox)
        self.horizontalLayout_m8.addWidget(self.ymoveLabel)
        self.verticalLayout_3.addItem(spacerItem)
        self.ymoveDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.moveGroupBox)
        self.ymoveDoubleSpinBox.setDecimals(3)
        self.ymoveDoubleSpinBox.setMinimum(-10.0)
        self.ymoveDoubleSpinBox.setMaximum(10.0)
        self.horizontalLayout_m8.addWidget(self.ymoveDoubleSpinBox)
        self.verticalLayout_3.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_m8)

        self.horizontalLayout_m9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_m9.addItem(spacerItem)
        self.zmoveLabel = QtWidgets.QLabel('z', self.moveGroupBox)
        self.zmoveLabel.setObjectName("zmoveLabel")
        self.horizontalLayout_m9.addWidget(self.zmoveLabel)
        self.zmoveDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.moveGroupBox)
        self.zmoveDoubleSpinBox.setDecimals(3)
        self.zmoveDoubleSpinBox.setMinimum(-15.0)
        self.zmoveDoubleSpinBox.setMaximum(2.4)
        self.horizontalLayout_m9.addWidget(self.zmoveDoubleSpinBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_m9)  # horizontallayout_7: xmovelabel+xdoublespinbox

        self.verticalLayout_3.addItem(spacerItem4)

        self.horizontalLayout_m10 = QtWidgets.QHBoxLayout()
        self.movelabel = QtWidgets.QLabel(self.moveGroupBox)
        self.movelabel.setText('Rel_Abs')
        self.horizontalLayout_m10.addWidget(self.movelabel)
        self.moveComboBox = QtWidgets.QComboBox(self.moveGroupBox)
        self.moveComboBox.setObjectName("moveComboBox")
        self.moveComboBox.addItems(['Rel', 'Abs'])
        self.horizontalLayout_m10.addWidget(self.moveComboBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_m10)
        self.verticalLayout_3.addItem(spacerItem4)

        self.horizontalLayout_m11 = QtWidgets.QHBoxLayout()
        self.vtype = QtWidgets.QLabel("velocity",self.moveGroupBox)
        self.horizontalLayout_m11.addWidget(self.vtype)
        self.VDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.moveGroupBox)
        self.VDoubleSpinBox.setDecimals(3)
        self.VDoubleSpinBox.setMinimum(0.000)
        self.VDoubleSpinBox.setMaximum(2.590)
        self.horizontalLayout_m11.addWidget(self.VDoubleSpinBox)
        self.VON_OFF = QtWidgets.QPushButton("OFF",self.moveGroupBox)
        self.VON_OFF.setCheckable(True)
        self.horizontalLayout_m11.addWidget(self.VON_OFF)
        self.verticalLayout_3.addLayout(self.horizontalLayout_m11)

        self.horizontalLayout_m12 = QtWidgets.QHBoxLayout()
        self.Vlimit=QtWidgets.QLabel(self.moveGroupBox)
        self.horizontalLayout_m12.addWidget(self.Vlimit)
        self.verticalLayout_3.addItem(spacerItem1)

        self.horizontalLayout_m12.addItem(spacerItem)
        self.goButton = QtWidgets.QPushButton('Go', self.moveGroupBox)
        self.horizontalLayout_m12.addWidget(self.goButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_m12)
        self.gridLayout.addWidget(self.moveGroupBox, 2, 0, 1, 1)

# gridlayout--verticallayout_8--downbutton
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.downSButton = QtWidgets.QPushButton(self)
        self.downSButton.setMinimumSize(QtCore.QSize(66, 52))
        self.downSButton.setMaximumSize(QtCore.QSize(66, 52))
        self.downSButton.setIcon(
            QtGui.QIcon("D:\storm-control-python3_pyqt5\storm-control-python3_pyqt5\storm_control\hal4000\icons\\1downarrow1-128.png"))
        self.downSButton.setIconSize(QtCore.QSize(56, 56))
        self.downSButton.setObjectName("backwardSButton")
        self.verticalLayout_8.addWidget(self.downSButton)

        self.downLButton = QtWidgets.QPushButton(self)
        self.downLButton.setMinimumSize(QtCore.QSize(66, 68))
        self.downLButton.setMaximumSize(QtCore.QSize(66, 68))
        self.downLButton.setIcon(
            QtGui.QIcon("D:\storm-control-python3_pyqt5\storm-control-python3_pyqt5\storm_control\hal4000\icons\\2dowarrow-128.png"))
        self.downLButton.setIconSize(QtCore.QSize(56, 56))
        self.downLButton.setObjectName("backwardLButton")
        self.verticalLayout_8.addWidget(self.downLButton)
        self.gridLayout.addLayout(self.verticalLayout_8, 2, 1, 1, 1)

        # piezo ui
        self.piezoGroupBox = QtWidgets.QGroupBox("piezo stage",self)
        self.verticalLayout_piezo = QtWidgets.QVBoxLayout(self.piezoGroupBox)
        self.verticalLayout_piezo.addItem(spacerItem)
        self.horizontalLayout_p1 = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel('z_abs', self.piezoGroupBox)
        self.horizontalLayout_p1.addWidget(self.label)

        self.piezo_doublespinbox = QtWidgets.QDoubleSpinBox(self.piezoGroupBox)
        self.piezo_doublespinbox.setDecimals(1)
        self.piezo_doublespinbox.setMinimum(-200.0)
        self.piezo_doublespinbox.setMaximum(200.0)
        self.horizontalLayout_p1.addWidget(self.piezo_doublespinbox)

        self.piezo_go = QtWidgets.QPushButton('GO', self.piezoGroupBox)
        self.horizontalLayout_p1.addWidget(self.piezo_go)
        self.verticalLayout_piezo.addLayout(self.horizontalLayout_p1)
        self.verticalLayout_piezo.addItem(spacerItem)

        self.horizontalLayout_p3=QtWidgets.QHBoxLayout(self.piezoGroupBox)
        self.zrel_label=QtWidgets.QLabel("z_Rel",self.piezoGroupBox)
        self.horizontalLayout_p3.addWidget(self.zrel_label)

        self.zReldoublespinbox=QtWidgets.QDoubleSpinBox()
        self.zReldoublespinbox.setMaximum(200)
        self.zReldoublespinbox.setValue(0)
        self.horizontalLayout_p3.addWidget(self.zReldoublespinbox)

        self.zRel_button=QtWidgets.QPushButton("Go",self.piezoGroupBox)
        self.horizontalLayout_p3.addWidget(self.zRel_button)
        self.verticalLayout_piezo.addLayout(self.horizontalLayout_p3)
        self.verticalLayout_piezo.addItem(spacerItem)

        self.horizontalLayout_p2 = QtWidgets.QHBoxLayout(self.piezoGroupBox)
        self.piezo_postext = QtWidgets.QLabel("position:   ",self.piezoGroupBox)
        self.horizontalLayout_p2.addWidget(self.piezo_postext)
        self.verticalLayout_piezo.addLayout(self.horizontalLayout_p2)
        self.verticalLayout_piezo.addItem(spacerItem)

        self.horizontalLayout_p4 = QtWidgets.QHBoxLayout(self.piezoGroupBox)
        self.rangelabel=QtWidgets.QLabel("range:    ",self.piezoGroupBox)
        self.horizontalLayout_p4.addWidget(self.rangelabel)
        self.verticalLayout_piezo.addLayout(self.horizontalLayout_p4)
        self.verticalLayout_piezo.addItem(spacerItem)

        horizontalLayout_updown=QtWidgets.QHBoxLayout(self.piezoGroupBox)
        self.piezo_up_button=QtWidgets.QPushButton('up',self.piezoGroupBox)
        self.piezo_down_button=QtWidgets.QPushButton('down',self.piezoGroupBox)
        horizontalLayout_updown.addWidget(self.piezo_up_button)
        horizontalLayout_updown.addWidget(self.piezo_down_button)
        self.verticalLayout_piezo.addLayout(horizontalLayout_updown)
        self.verticalLayout_piezo.addItem(spacerItem)

        horizontalLayout_p = QtWidgets.QHBoxLayout()
        label_p = QtWidgets.QLabel('move step', self.piezoGroupBox)
        self.step = QtWidgets.QDoubleSpinBox(self.piezoGroupBox)
        self.step.setDecimals(3)
        self.step.setMinimum(0)
        self.step.setMaximum(10)
        self.step.setValue(0.5)
        horizontalLayout_p.addWidget(label_p)
        horizontalLayout_p.addWidget(self.step)
        self.verticalLayout_piezo.addLayout(horizontalLayout_p)

        self.gridLayout.addWidget(self.piezoGroupBox, 2, 2, 1,1)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    example = stageUI()
    sys.exit(app.exec_())