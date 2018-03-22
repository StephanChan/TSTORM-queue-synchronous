
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys
import GraphicsView
import GraphicsScene

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupMainWindow()
        self.show()



    def setupMainWindow(self):
        self.setWindowTitle("main window")
        self.setMinimumSize(QtCore.QSize(900, 700))
        self.setMaximumSize(QtCore.QSize(1000, 100))
        self.gridLayout = QtWidgets.QGridLayout(self)
# menu
        horizontalLayout_1 = QHBoxLayout()
        spacerItem = QSpacerItem(100, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.shutterButton = QPushButton('shutter', self)
        self.AOTFButton = QPushButton('AOTF', self)
        self.GalvoButton = QPushButton('Galvo', self)
        self.StageButton = QPushButton('stage', self)
        horizontalLayout_1.addWidget(self.shutterButton)
        horizontalLayout_1.addItem(spacerItem)
        horizontalLayout_1.addWidget(self.AOTFButton)
        horizontalLayout_1.addItem(spacerItem)
        horizontalLayout_1.addWidget(self.GalvoButton)
        horizontalLayout_1.addItem(spacerItem)
        horizontalLayout_1.addWidget(self.StageButton)
        horizontalLayout_1.addItem(spacerItem)
        self.gridLayout.addLayout(horizontalLayout_1, 0, 0, 1, 4)
#set camera mode
        '''cambox=QGroupBox('camera box',self)
        verticalLayout_c=QVBoxLayout(cambox)
        #trigger source
        horizontalLayout_c1=QHBoxLayout()
        label_source=QLabel('trigger source',cambox)
        self.source=QComboBox(cambox)
        self.source.addItems(['external','internal'])
        horizontalLayout_c1.addWidget(label_source)
        horizontalLayout_c1.addWidget(self.source)
        #trigger active
        horizontalLayout_c2=QHBoxLayout()
        label_active=QLabel('trigger active',cambox)
        self.active=QComboBox(cambox)
        self.active.addItems(['edge','synchronous'])
        horizontalLayout_c2.addWidget(label_active)
        horizontalLayout_c2.addWidget(self.active)
        #set button
        horizontalLayout_c3=QHBoxLayout()
        self.set_button=QPushButton('set',cambox)
        horizontalLayout_c3.addWidget(self.set_button)
        verticalLayout_c.addLayout(horizontalLayout_c1)
        verticalLayout_c.addLayout(horizontalLayout_c2)
        verticalLayout_c.addLayout(horizontalLayout_c3)
        cambox.setLayout(verticalLayout_c)
        self.gridLayout.addWidget(cambox)'''
# handle live
        liveGroupBox = QGroupBox("live box",self)
        verticalLayout_l = QVBoxLayout(liveGroupBox)
        # camera exposure
        horizontalLayout_l2=QHBoxLayout()
        horizontalLayout_l22 = QHBoxLayout()
        label_cam_expo=QLabel("cam_exposure",liveGroupBox)
        self.cam_expo=QDoubleSpinBox(liveGroupBox)
        self.cam_expo.setDecimals(0)
        self.cam_expo.setMinimum(5)
        self.cam_expo.setMaximum(1000)
        self.cam_expo.setValue(50)
        horizontalLayout_l2.addWidget(label_cam_expo)
        horizontalLayout_l2.addWidget(self.cam_expo)
        #live button and autoscale button
        horizontalLayout_l4=QHBoxLayout()
        self.liveButton = QPushButton('live', self)
        self.liveButton.setCheckable(True)
        self.autoscalebutton = QPushButton("autoscale", liveGroupBox)
        horizontalLayout_l4.addWidget(self.liveButton)
        horizontalLayout_l4.addWidget(self.autoscalebutton)
        horizontalLayout_15=QHBoxLayout()
        label=QLabel('max',liveGroupBox)
        self.slider_up = QSlider(QtCore.Qt.Horizontal, self)
        self.slider_up.setRange(0, 30000)
        horizontalLayout_15.addWidget(label)
        horizontalLayout_15.addWidget(self.slider_up)

        horizontalLayout_16=QHBoxLayout()
        label_=QLabel('min',liveGroupBox)
        self.slider_down = QSlider(QtCore.Qt.Horizontal, self)
        self.slider_down.setRange(0, 10000)
        horizontalLayout_16.addWidget(label_)
        horizontalLayout_16.addWidget(self.slider_down)

        verticalLayout_l.addLayout(horizontalLayout_l2)
        verticalLayout_l.addLayout(horizontalLayout_l22)
        #verticalLayout_l.addLayout(horizontalLayout_l3)
        #verticalLayout_l.addLayout(horizontalLayout_l33)
        verticalLayout_l.addLayout(horizontalLayout_l4)
        verticalLayout_l.addLayout(horizontalLayout_15)
        verticalLayout_l.addLayout(horizontalLayout_16)
        liveGroupBox.setLayout(verticalLayout_l)
        self.gridLayout.addWidget(liveGroupBox,1,0,1,1)
# handle record
        recordGroupBox = QGroupBox("record box",self)
        verticalLayout_r = QVBoxLayout(recordGroupBox)
        #isolated record
        horizontalLayout_i1=QHBoxLayout()
        self.IrecordButton=QPushButton('isolated_record',self)
        self.IrecordButton.setCheckable(True)
        horizontalLayout_i1.addWidget(self.IrecordButton)

        horizontalLayout_i2=QHBoxLayout()
        label_Icam_expo=QLabel("cam_expo", recordGroupBox)
        self.Icam_expo = QDoubleSpinBox(recordGroupBox)
        self.Icam_expo.setDecimals(0)
        self.Icam_expo.setMinimum(0)
        self.Icam_expo.setMaximum(200)
        self.Icam_expo.setValue(30)
        horizontalLayout_i2.addWidget(label_Icam_expo)
        horizontalLayout_i2.addWidget(self.Icam_expo)
        spacerItem = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)

        #connect
        #horizontalLayout_r0 = QHBoxLayout()
        #self.connectButton = QPushButton('connect', self)
        #horizontalLayout_r0.addWidget(self.connectButton)
        # 405
        horizontalLayout_r1 = QHBoxLayout()
        label_405_expo = QLabel("405_expo", recordGroupBox)
        self.r_405_expo = QDoubleSpinBox(recordGroupBox)
        self.r_405_expo.setDecimals(0)
        self.r_405_expo.setMinimum(0)
        self.r_405_expo.setMaximum(2000)
        self.r_405_expo.setValue(100)

        horizontalLayout_r1.addWidget(label_405_expo)
        horizontalLayout_r1.addWidget(self.r_405_expo)
        # 647
        horizontalLayout_r2 = QHBoxLayout()
        label_647_expo = QLabel("647_expo", recordGroupBox)
        self.r_647_expo = QDoubleSpinBox(recordGroupBox)
        self.r_647_expo.setDecimals(0)
        self.r_647_expo.setMinimum(0)
        self.r_647_expo.setMaximum(2000)
        self.r_647_expo.setValue(100)

        horizontalLayout_r2.addWidget(label_647_expo)
        horizontalLayout_r2.addWidget(self.r_647_expo)
        # camera exposure
        horizontalLayout_r3 = QHBoxLayout()
        label_cam_expo = QLabel("cam_expo", recordGroupBox)
        self.rcam_expo = QDoubleSpinBox(recordGroupBox)
        self.rcam_expo.setDecimals(0)
        self.rcam_expo.setMinimum(5)
        self.rcam_expo.setMaximum(1000)
        self.rcam_expo.setValue(30)
        horizontalLayout_r3.addWidget(label_cam_expo)
        horizontalLayout_r3.addWidget(self.rcam_expo)

        # frames and cycles
        horizontalLayout_r4 = QHBoxLayout()
        label_frames = QLabel("frames", recordGroupBox)
        self.rframes = QDoubleSpinBox(recordGroupBox)
        self.rframes.setDecimals(0)
        self.rframes.setMinimum(1)
        self.rframes.setMaximum(100)
        self.rframes.setValue(10)
        label_cycles = QLabel("cycles", recordGroupBox)
        self.rcycles = QDoubleSpinBox(recordGroupBox)
        self.rcycles.setDecimals(0)
        self.rcycles.setMinimum(0)
        self.rcycles.setMaximum(1000)
        self.rcycles.setValue(5)
        horizontalLayout_r4.addWidget(label_frames)
        horizontalLayout_r4.addWidget(self.rframes)
        horizontalLayout_r4.addWidget(label_cycles)
        horizontalLayout_r4.addWidget(self.rcycles)
        #stage
        horizontalLayout_r5 = QHBoxLayout()
        label_range = QLabel("stage_range", recordGroupBox)
        self.range = QDoubleSpinBox(recordGroupBox)
        self.range.setDecimals(0)
        self.range.setMinimum(1)
        self.range.setMaximum(100)
        self.range.setValue(10)
        label_step = QLabel("step", recordGroupBox)
        self.step = QDoubleSpinBox(recordGroupBox)
        self.step.setDecimals(0)
        self.step.setMinimum(1)
        self.step.setMaximum(10)
        self.step.setValue(1)
        horizontalLayout_r5.addWidget(label_range)
        horizontalLayout_r5.addWidget(self.range)
        horizontalLayout_r5.addWidget(label_step)
        horizontalLayout_r5.addWidget(self.step)
        # record button
        horizontalLayout_r7 = QHBoxLayout()
        self.recordButton = QPushButton('syn_record', self)
        horizontalLayout_r7.addWidget(self.recordButton)
        #filename
        #horizontalLayout_r6=QHBoxLayout()
        #label_file=QLabel("file path",recordGroupBox)
        #self.name_text = QLineEdit('D:\\Data\\', recordGroupBox)
        #self.name_num = QDoubleSpinBox(recordGroupBox)
        #self.name_num.setDecimals(0)
        #self.name_num.setMinimum(1)
        #self.name_num.setMaximum(1000)
        #self.name_num.setValue(1)
        #horizontalLayout_r6.addWidget(label_file)
        #horizontalLayout_r6.addWidget(self.name_text)
       # horizontalLayout_r6.addWidget(self.name_num)

        #verticalLayout_r.addLayout(horizontalLayout_r0)
        verticalLayout_r.addLayout(horizontalLayout_i1)
        verticalLayout_r.addLayout(horizontalLayout_i2)
        verticalLayout_r.addItem(spacerItem)
        verticalLayout_r.addLayout(horizontalLayout_r1)
        verticalLayout_r.addLayout(horizontalLayout_r2)
        verticalLayout_r.addLayout(horizontalLayout_r3)
        verticalLayout_r.addLayout(horizontalLayout_r4)
        verticalLayout_r.addLayout(horizontalLayout_r5)
        #verticalLayout_r.addLayout(horizontalLayout_r6)
        verticalLayout_r.addLayout(horizontalLayout_r7)

        recordGroupBox.setLayout(verticalLayout_r)
        self.gridLayout.addWidget(recordGroupBox, 2, 0, 2, 1)

        # display image window
        self.livewindow = GraphicsView.QtCameraGraphicsView()
        self.scene=QtWidgets.QGraphicsScene(self)
        self.scene.setSceneRect(0,0,600,600)
        self.item=GraphicsScene.QtCameraGraphicsItem()
        self.scene.addItem(self.item)
        self.livewindow.setScene(self.scene)

        #self.livewindow.setScaledContents(True)
        #data = np.ones((2048,2048), dtype=np.uint8)
        #pixmap = QtGui.QImage(data, 2048, 2048, QtGui.QImage.Format_Indexed8)
        #pixmap = QtGui.QPixmap.fromImage(pixmap)
        #self.item.updateImageWithFrame(pixmap)
        #self.livewindow.setPixmap(pixmap)
        self.gridLayout.addWidget(self.livewindow,1,1,3,1)

        horizontalLayout_message = QHBoxLayout()
        # message label
        self.message_label = QLabel('message', self)
        horizontalLayout_message.addWidget(self.message_label)
        self.gridLayout.addLayout(horizontalLayout_message, 7, 0, 1, 3)


        self.recordButton.setCheckable(True)

def update():
        for i in range(100):
            num = random.randint(0, 300)
            data = np.ones((2048,2048), dtype=np.uint8) * num
            pixmap = QtGui.QImage(data, 2048, 2048, QtGui.QImage.Format_Indexed8)
            pixmap = QtGui.QPixmap.fromImage(pixmap)
            example.item.updateImageWithFrame(pixmap)
            # app.processEvents()
            # ex.camera_view.viewport().repaint()
            time.sleep(0.3)
            print(i)


if __name__ == '__main__':
    import random
    import time
    import threading
    app = QApplication(sys.argv)
    example = MainWindow()
    #example.livewindow.click_on_pixel.connect(example.item.getIntensityInfo)
    thread = threading.Thread(target=update)
    thread.start()
    sys.exit(app.exec_())