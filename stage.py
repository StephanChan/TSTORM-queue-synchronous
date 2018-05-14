from PyQt5 import QtCore, QtGui, QtWidgets
import stage_UI as ui
import pyapt
import threading
import time
import mymclController as mcl
import sys

class Stage(QtWidgets.QWidget):
    signal=QtCore.pyqtSignal(float)
    def __init__(self):
        super().__init__()
        self.is_stage_runing=None
        self.ui=ui.stageUI()
        self.ui.setupUI()
        self.ui.show()
        #init stage handle, need several seconds to do it
        '''self.handle_x = pyapt.APTMotor(83833850)
        self.handle_y = pyapt.APTMotor(83840820)
        self.handle_z = pyapt.APTMotor(83841441)
        self.timer = QtCore.QTimer()#a timer, periodically call function
        self.timer.timeout.connect(lambda: self.readinfo())
        self.timer.start(20)#timer set 20 ms'''
        #set stage range
        '''self.handle_x.setStageAxisInformation(-2, 4)
        self.handle_y.setStageAxisInformation(-1, 3)
        self.handle_z.setStageAxisInformation(-20, 5)'''
        #piezo stage handle
        self.mcl_handle = mcl.MCLStage(mcl_lib="C:\Program Files\Mad City Labs\\NanoDrive\Madlib.dll")
#put stage range and velocity range on GUI
        '''self.ui.xrangeLabel.setText('x range: '+'min: ' +str(self.handle_x.getStageAxisInformation()[0]) +
                                  ',   max: ' + str(self.handle_x.getStageAxisInformation()[1]))
        self.ui.yrangeLabel.setText('y range: '+'min: ' +str(self.handle_y.getStageAxisInformation()[0]) +
                                ',   max: ' + str(self.handle_y.getStageAxisInformation()[1]))
        self.ui.zrangeLabel.setText('z range: '+'min: ' +str(self.handle_z.getStageAxisInformation()[0]) +
                                ',   max: ' + str(format(self.handle_z.getStageAxisInformation()[1], '.3f')))
        self.ui.Vlimit.setText('max_acc:' + str(self.handle_y.getVelocityParameterLimits()[0]) + ' max_V:' + str(
            format(self.handle_y.getVelocityParameterLimits()[1], '.2f')))'''
        self.ui.rangelabel.setText('z range: ' + str(self.mcl_handle._getCalibration(3)))

        '''self.ui.VON_OFF.clicked.connect(lambda: self.VON_OFFstate())
        self.ui.zupButton.clicked.connect(lambda: self.ZUP())
        self.ui.zupLButton.clicked.connect(lambda: self.ZUPL())
        self.ui.zdownButton.clicked.connect(lambda: self.ZDOWN())
        self.ui.zdownLButton.clicked.connect(lambda: self.ZDOWNL())
        self.ui.upLButton.clicked.connect(lambda: self.XUPL())
        self.ui.upSButton.clicked.connect(lambda: self.XUP())
        self.ui.downLButton.clicked.connect(lambda: self.XDOWNL())
        self.ui.downSButton.clicked.connect(lambda: self.XDOWN())
        self.ui.leftLButton.clicked.connect(lambda: self.YLEFTL())
        self.ui.leftSButton.clicked.connect(lambda: self.YLEFT())
        self.ui.rightLButton.clicked.connect(lambda: self.YRIGHTL())
        self.ui.rightSButton.clicked.connect(lambda: self.YRIGHT())'''
        self.ui.exitButton.clicked.connect(lambda: self.Exit())

        self.piezo_timer = QtCore.QTimer()
        self.piezo_timer.timeout.connect(lambda: self.piezoinfo())
        self.piezo_timer.start(50)
        self.ui.goButton.clicked.connect(lambda: self.GO())
        self.ui.piezo_go.clicked.connect(lambda: self.piezo_Abs(distance=float(self.ui.piezo_doublespinbox.text())))
        self.ui.zRel_button.clicked.connect(lambda: self.piezo_Rel(distance=float(self.ui.zReldoublespinbox.text())))
        self.ui.piezo_up_button.clicked.connect(lambda: self.piezo_up())
        self.ui.piezo_down_button.clicked.connect(lambda: self.piezo_down())
#action in synchronous recording only
    def run(self,step):
        print('stage is doing work')
        self.piezo_Rel(step)
        time.sleep(0.5)

#move Z axis
    def ZUP(self):
        self.handle_z.mRel(float(self.ui.small_step.text()))

    def ZUPL(self):
        self.handle_z.mRel(float(self.ui.big_step.text()))

    def ZDOWN(self):
        self.handle_z.mRel(-float(self.ui.small_step.text()))

    def ZDOWNL(self):
        self.handle_z.mRel(-float(self.ui.big_step.text()))

    def XUP(self):
        self.handle_y.mRel(-float(self.ui.small_step.text()))
        pass

    def XUPL(self):
        self.handle_y.mRel(-float(self.ui.big_step.text()))
        pass

    def XDOWN(self):
        self.handle_y.mRel(float(self.ui.small_step.text()))
        pass

    def XDOWNL(self):
        self.handle_y.mRel(float(self.ui.big_step.text()))
        pass

    def YLEFT(self):
        self.handle_x.mRel(-float(self.ui.small_step.text()))

    def YLEFTL(self):
        self.handle_x.mRel(-float(self.ui.big_step.text()))

    def YRIGHT(self):
        self.handle_x.mRel(float(self.ui.small_step.text()))

    def YRIGHTL(self):
        self.handle_x.mRel(float(self.ui.big_step.text()))

    def HOME(self):
        self.handle_x.mAbs(0)
        self.handle_y.mAbs(0)
        self.handle_z.mAbs(0)

#get stage current position
    def readinfo(self):
        self.ui.xposLabel.setText("x position: " +str(format(self.handle_x.getPos(), '.3f')))
        self.ui.yposLabel.setText("y position: " + str(format(self.handle_y.getPos(), '.3f')))
        self.ui.zposLabel.setText("z position: " + str(format(self.handle_z.getPos(), '.3f')))

#turn on/off the velocity control
    def VON_OFFstate(self):
        if self.ui.VON_OFF.isChecked():
            self.ui.VON_OFF.setText('ON')

        else:
            self.ui.VON_OFF.setText('OFF')

#customized move stage
    def GO(self):
        if self.ui.moveComboBox.currentText() == 'Rel':
            if self.ui.VON_OFF.isChecked():
                self.handle_x.mcRel(float(self.ui.xmoveDoubleSpinBox.text()), float(self.ui.VDoubleSpinBox.text()))
                self.handle_y.mcRel(float(self.ui.ymoveDoubleSpinBox.text()), float(self.ui.VDoubleSpinBox.text()))
                self.handle_z.mcRel(float(self.ui.zmoveDoubleSpinBox.text()), float(self.ui.VDoubleSpinBox.text()))

            else:
                self.handle_x.mRel(float(self.ui.xmoveDoubleSpinBox.text()))
                self.handle_y.mRel(float(self.ui.ymoveDoubleSpinBox.text()))
                self.handle_z.mRel(float(self.ui.zmoveDoubleSpinBox.text()))
        else:
            if self.ui.VON_OFF.isChecked():
                self.handle_x.mcAbs(float(self.ui.xmoveDoubleSpinBox.text()), float(self.ui.VDoubleSpinBox.text()))
                self.handle_y.mcAbs(float(self.ui.ymoveDoubleSpinBox.text()), float(self.ui.VDoubleSpinBox.text()))
                self.handle_z.mcAbs(float(self.ui.zmoveDoubleSpinBox.text()), float(self.ui.VDoubleSpinBox.text()))

            else:
                self.handle_x.mAbs(float(self.ui.xmoveDoubleSpinBox.text()))
                self.handle_y.mAbs(float(self.ui.ymoveDoubleSpinBox.text()))
                self.handle_z.mAbs(float(self.ui.zmoveDoubleSpinBox.text()))

#shut down the stage handle
    def Exit(self):
        '''self.timer.stop()
        self.handle_x.cleanUpAPT()
        self.handle_y.cleanUpAPT()
        self.handle_z.cleanUpAPT()'''
        self.mcl_handle.shutDown()

#move piezo to absolute position
    def piezo_Abs(self,distance):
        self.mcl_handle.moveTo(3,distance)

#move piezo to relevant position
    def piezo_Rel(self,distance=0.0):
        position=self.mcl_handle.getPosition(3)
        self.mcl_handle.moveTo(3,distance+position)


    def piezoinfo(self):
        self.ui.piezo_postext.setText("z_posi=" + str(format(self.mcl_handle.getPosition(3), '.3f')))

    def piezo_up(self):
        self.piezo_Rel(distance=float(self.ui.step.text()))

    def piezo_down(self):
        self.piezo_Rel(distance=-float(self.ui.step.text()))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Stage()
    sys.exit(app.exec_())