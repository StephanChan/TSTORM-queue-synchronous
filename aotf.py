from PyQt5.QtWidgets import *
import PyQt5.QtWidgets as QtWidgets
import sys
import aotfUI as ui
import AOTF_API as aotf
import module

class Aotf(module.Module):
    def __init__(self,message):
        super().__init__(message)
        self.message=message
        self.ui=ui.aotfGui()
        self.ui.setupUI()
        self.AOTF_handle = aotf.AOTF()

        self.ui.button_analog.clicked.connect(lambda: self.analog())
        self.ui.button_run1.clicked.connect(lambda: self.channel_1_set())
        self.ui.button_run2.clicked.connect(lambda: self.channel_2_set())
        self.ui.button_run3.clicked.connect(lambda: self.channel_3_set())
        self.ui.button_run4.clicked.connect(lambda: self.channel_4_set())
        self.ui.button_run5.clicked.connect(lambda: self.channel_5_set())
        self.ui.button_run6.clicked.connect(lambda: self.channel_6_set())
        self.ui.button_run7.clicked.connect(lambda: self.channel_7_set())
        self.ui.button_run8.clicked.connect(lambda: self.channel_8_set())

    def channel_1_set(self):
        if self.ui.button_run1.isChecked():
            if self.ui.textbox_f1.text() != "" and self.ui.textbox_a1.text() != "":
                self.ui.button_run1.setText('OFF')
                self.AOTF_handle.setFrequency(1, float(self.ui.textbox_f1.text()))
                self.AOTF_handle.setAmplitude(1, float(self.ui.textbox_a1.text()))
                self.AOTF_handle.channelOnOff(1, 1)
        else:
            self.AOTF_handle.channelOnOff(1, 0)
            self.ui.button_run1.setText('Run')

    def channel_2_set(self):
        if self.ui.button_run2.isChecked():
            if self.ui.textbox_f2.text() != "" and self.ui.textbox_a2.text() != "":
                self.ui.button_run2.setText('OFF')
                self.AOTF_handle.setFrequency(2, float(self.ui.textbox_f2.text()))
                self.AOTF_handle.setAmplitude(2, float(self.ui.textbox_a2.text()))
                self.AOTF_handle.channelOnOff(2, 1)
        else:
            self.AOTF_handle.channelOnOff(2, 0)
            self.ui.button_run2.setText('Run')

    def channel_3_set(self):
        if self.ui.button_run3.isChecked():
            if self.ui.textbox_f3.text() != "" and self.ui.textbox_a3.text() != "":
                self.ui.button_run3.setText('OFF')
                self.AOTF_handle.setFrequency(3, float(self.ui.textbox_f3.text()))
                self.AOTF_handle.setAmplitude(3, float(self.ui.textbox_a3.text()))
                self.AOTF_handle.channelOnOff(3, 1)
        else:
            self.AOTF_handle.channelOnOff(3, 0)
            self.ui.button_run3.setText('Run')

    def channel_4_set(self):
        if self.ui.button_run4.isChecked():
            if self.ui.textbox_f4.text() != "" and self.ui.textbox_a4.text() != "":
                self.ui.button_run4.setText('OFF')
                self.AOTF_handle.setFrequency(4, float(self.ui.textbox_f4.text()))
                self.AOTF_handle.setAmplitude(4, float(self.ui.textbox_a4.text()))
                self.AOTF_handle.channelOnOff(4, 1)
        else:
            self.AOTF_handle.channelOnOff(4, 0)
            self.ui.button_run4.setText('Run')

    def channel_5_set(self):
        if self.ui.button_run5.isChecked():
            if self.ui.textbox_f5.text() != "" and self.ui.textbox_a5.text() != "":
                self.ui.button_run5.setText('OFF')
                self.AOTF_handle.setFrequency(5, float(self.ui.textbox_f5.text()))
                self.AOTF_handle.setAmplitude(5, float(self.ui.textbox_a5.text()))
                self.AOTF_handle.channelOnOff(5, 1)
        else:
            self.AOTF_handle.channelOnOff(5, 0)
            self.ui.button_run5.setText('Run')

    def channel_6_set(self):
        if self.ui.button_run6.isChecked():
            if self.ui.textbox_f6.text() != "" and self.ui.textbox_a6.text() != "":
                self.ui.button_run6.setText('OFF')
                self.AOTF_handle.setFrequency(6, float(self.ui.textbox_f6.text()))
                self.AOTF_handle.setAmplitude(6, float(self.ui.textbox_a6.text()))
                self.AOTF_handle.channelOnOff(6, 1)
        else:
            self.AOTF_handle.channelOnOff(6, 0)
            self.ui.button_run6.setText('Run')

    def channel_7_set(self):
        if self.ui.button_run7.isChecked():
            if self.ui.textbox_f7.text() != "" and self.ui.textbox_a7.text() != "":
                self.ui.button_run7.setText('OFF')
                self.AOTF_handle.setFrequency(7, float(self.ui.textbox_f7.text()))
                self.AOTF_handle.setAmplitude(7, float(self.ui.textbox_a7.text()))
                self.AOTF_handle.channelOnOff(7, 1)
        else:
            self.AOTF_handle.channelOnOff(7, 0)
            self.ui.button_run7.setText('Run')

    def channel_8_set(self):
        if self.ui.button_run8.isChecked():
            if self.ui.textbox_f8.text() != "" and self.ui.textbox_a8.text() != "":
                self.ui.button_run8.setText('OFF')
                self.AOTF_handle.setFrequency(8, float(self.ui.textbox_f8.text()))
                self.AOTF_handle.setAmplitude(8, float(self.ui.textbox_a8.text()))
                self.AOTF_handle.channelOnOff(8, 1)
        else:
            self.AOTF_handle.channelOnOff(8, 0)
            self.ui.button_run8.setText('Run')

    def shutdown(self):
        self.AOTF_handle.shutdown()


    def analog(self):

            if self.ui.button_analog.isChecked():
                self.ui.button_analog.setText('external')
                self.AOTF_handle.analogModulationOn()

            else:
                self.ui.button_analog.setText('internal')
                self.AOTF_handle.analogModulationOff()

if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    ex=Aotf({})
    sys.exit(app.exec_())