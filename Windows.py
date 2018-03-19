import hamamatsu_camera as cam
import tifffile as tiff
import numpy as np
import c_image_manipulation_c as c_image
import time
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import PyDAQmx
import ctypes
import sys
import datetime
import os
import time as Time
from multiprocessing import Queue

import windowUI as ui

import aotf as aotfui
import stage as Stage
import message
import shutter as shutter
import galvo as Galvo
import synchronization as syn
import tinytiffwriter
import tifffile
import libtiff


class MainWindow:
    def __init__(self):
        super().__init__()
        self.ui=ui.MainWindow()
        self.ui.setupMainWindow()
        self.ui.show()
        self.queue = Queue()
        self.frames = []
        self.lines = None
        self.live_thread_flag = None
        self.record_thread_flag = None
        self.filepath = 'D:\\Data\\'
        self.filename = None
        self.rescale_min = 0
        self.rescale_max = 65535
        self.lock = threading.Lock()
        self.hcam = cam.HamamatsuCameraMR(camera_id=0)

        self.ui.shutterButton.clicked.connect(lambda: self.shutterUi())
        self.ui.AOTFButton.clicked.connect(lambda: self.aotfUi())
        self.ui.GalvoButton.clicked.connect(lambda: self.galvoUi())
        self.ui.StageButton.clicked.connect(lambda: self.stageUi())
        self.ui.liveButton.clicked.connect(lambda: self.live_state_change())
        self.ui.recordButton.clicked.connect(lambda: self.record_state_change())
        self.ui.IrecordButton.clicked.connect(lambda: self.Irecord_state_change())
        self.ui.autoscalebutton.clicked.connect(lambda: self.autoscale())
        self.ui.slider_up.valueChanged.connect(lambda: self.upscale())
        self.ui.slider_down.valueChanged.connect(lambda: self.downscale())

        self.live_thread = threading.Thread(target=self.display, name='liveThread')
        self.record_thread = threading.Thread(target=self.recording, name="recordThread")


    def autoscale(self):
        try:
            self.rescale_min = self.image_min
            self.rescale_max = self.image_max
        except:
            print("not start display yet")

    def upscale(self):
        self.rescale_max=self.ui.slider_up.value()

    def downscale(self):
        self.rescale_min=self.ui.slider_down.value()

    '''def get_buffer(self):
            [self.frames, dims] = self.hcam.getFrames()
            print(str(len(self.frames)) + "  frames get")
            # pid = os.getpid()
            # print("main PID: " + str(pid))
            #print("buffer thread id: " + str(threading.current_thread().name))
            if self.live_thread_flag == True:
                if self.live_thread.is_alive():
                    print("shutting down living thread")
                else:
                    self.live_thread = threading.Thread(target=self.display, name='liveThread')
                    self.live_thread.start()

            if self.record_thread_flag == True:
                if self.record_thread.is_alive():
                    print("recording not finished,data losed")
                else:
                    self.record_thread = threading.Thread(target=self.recording, name="recordThread")
                    self.record_thread.start()'''

    def get_buffer(self,event_live,event_record):
            [self.frames, dims] = self.hcam.getFrames()
            print(str(len(self.frames)) + "  frames get")
            if self.live_thread_flag == True:
                event_live.set()

            if self.record_thread_flag == True:
                event_record.set()




    def buffer_thread(self,event_live,event_record):
        while(self.live_thread_flag==True):
            #start = time.clock()
            time.sleep(0.15)
            self.get_buffer(event_live,event_record)
            #stop = time.clock()
            #print('time: ',stop-start)


    def live_state_change(self):
            if self.ui.liveButton.isChecked():
                try:
                    self.disconnect()
                except:
                    pass

                self.start_living()
            else:
                self.stop_living()


    def start_living(self):
        self.ui.liveButton.setText('stop live')
        self.live_thread_flag = True
        self.hcam.startAcquisition()
        self.hcam.setPropertyValue('exposure_time', float(self.ui.cam_expo.text()) / 1000.0)
        self.event_live=threading.Event()
        self.event_record=threading.Event()
        self.get_buffer_thread = threading.Thread(target=self.buffer_thread, args=(self.event_live,self.event_record), name='buffer thread')
        self.get_buffer_thread.start()
        self.live_thread = threading.Thread(target=self.display, args=(self.event_live,), name='liveThread')
        self.live_thread.start()


    def stop_living(self):
        self.live_thread_flag = False
        self.event_live.clear()
        self.hcam.stopAcquisition()
        self.ui.liveButton.setText('Live')


    def display(self,event):
        '''live child thread
                    display images when one cycle ends'''
        # pid = os.getpid()
        # print("living PID: " + str(pid))
        # print("living thread id: "+str(threading.current_thread().name))
        while (self.live_thread_flag == True):
            event.wait()
            event.clear()
            image = self.frames[0].np_array.reshape((2048, 2048))
            self.lock.acquire()
            rescale_min = self.rescale_min
            rescale_max = self.rescale_max
            [temp, self.image_min, self.image_max] = c_image.rescaleImage(image,
                                                                          False,
                                                                          False,
                                                                          False,
                                                                          [rescale_min, rescale_max],
                                                                          None)
            self.lock.release()
            qImg = QtGui.QImage(temp.data, 2048, 2048, QtGui.QImage.Format_Indexed8)
            pixmap01 = QtGui.QPixmap.fromImage(qImg)
            self.ui.livewindow.setPixmap(pixmap01)



            # stop=time.clock()
            # print("time for one frame display: "+str(stop-start))

    # when record button is clicked, set record flag to True or False, then record thread will start or stop
    def Irecord_state_change(self):
        if not self.ui.IrecordButton.isChecked():#stop recording
            self.ui.IrecordButton.setText('isolated record')
            self.stop_record()
            #self.liveButton.setChecked(True)
            #self.live_state_change()
        else:
            time = datetime.datetime.now()
            self.filename = self.filepath + str(time)[:10] + '_' +str(time)[11:13]+'_'+str(time)[14:16]
            self.tiff = libtiff.TIFF.open(self.filename + '.tif', mode='w8')
            self.record_thread_flag = True
            self.record_thread = threading.Thread(target=self.recording, args=(self.event_record,), name="recordThread")
            self.record_thread.start()
            self.ui.IrecordButton.setText('stop')
            self.hcam.setPropertyValue('exposure_time', float(self.ui.Icam_expo.text())/1000.0)


    def record_state_change(self):
        if not self.ui.recordButton.isChecked():
            self.stop_record()
        else:
            self.connect()
            self.start_record()


    def disconnect(self):
        self.hcam.setPropertyValue("trigger_source", 1)
        self.aotf.ui.button_analog.setChecked(False)
        self.aotf.analog()


    def connect(self):
        if self.ui.liveButton.isChecked():
            self.stop_living()

        self.hcam.setPropertyValue("trigger_source", 2)
        self.hcam.setPropertyValue("trigger_active", 1)
        self.aotf.ui.button_analog.setChecked(True)
        self.aotf.analog()
        self.lines=syn.Lines(time_405=float(self.ui.r_405_expo.text()),time_647=float(self.ui.r_647_expo.text()),
                                   frames=float(self.ui.rframes.text()),
                             cycles=float(self.ui.rcycles.text()),exposure=float(self.ui.rcam_expo.text()))


    def recording(self,event):
        '''record child thread
        record frames when one cycle ends'''
        # start = time.clock()
        #print("record thread id: " + str(threading.current_thread()))
        num=0
        count=0
        while(self.record_thread_flag==True):
            event.wait()
            event.clear()
            for i in self.frames:
                num+=1
                if num>=800:
                    count+=1
                    self.tiff.close()
                    self.tiff=libtiff.TIFF.open(self.filename+'-'+str(count)+'.tif', mode='w8')
                    num=1
                if self.record_thread_flag == False:
                    return (0)
                image = i.np_array.reshape((2048, 2048))
                self.tiff.write_image(image)  # use libtiff
                # self.tiff.tinytiffwrite(image,self.file)
                # tifffile.imsave(self.filename, image) #use tifffile.py




    def start_record(self):
        self.lines.set_lines()
        #self.tiff = tinytiffwriter.tinytiffwriter()#use tinytiffwriter.dll
        #self.file = self.tiff.tinytiffopen(self.filename,16,2048,2048)
        time = datetime.datetime.now()
        self.filename = self.filepath + str(time)[:10] + '_' + str(time)[11:13] + '_' + str(time)[14:16]
        self.tiff = libtiff.TIFF.open(self.filename + '.tif', mode='w8')
        self.record_thread_flag = True
        self.live_thread_flag=True
        self.ui.recordButton.setText('stop')
        self.hcam.startAcquisition()
        self.hcam.setPropertyValue('exposure_time', float(self.ui.rcam_expo.text()) / 1000.0)
        for i in range(int(float(self.ui.range.text()) / float(self.ui.step.text()))):
            self.in_queue()
        self.synchronous_thread = Mythread(self.worker)
        self.get_buffer_thread = threading.Thread(target=self.buffer_thread, args=(self.event_live, self.event_record),
                                                  name='buffer thread')
        self.record_thread = threading.Thread(target=self.recording, args=(self.event_record,), name="recordThread")
        self.live_thread = threading.Thread(target=self.display, args=(self.event_live,), name='liveThread')
        self.live_thread.start()
        self.record_thread.start()
        self.synchronous_thread.start()
        self.get_buffer_thread.start()



    def in_queue(self):
        self.queue.put({'lines': 0})
        self.queue.put({'stage': float(self.ui.step.text())})


    def worker(self):
        while not self.queue.empty():
            if self.record_thread_flag==True:
                item = self.queue.get()
                module = getattr(self, str(list(item.keys())[0]))
                module.run(item[str(list(item.keys())[0])])
                time.sleep(0.1)
            else:
                break

        self.stop_record()


    def stop_record(self):
        self.event_live.clear()
        self.event_record.clear()
        self.record_thread_flag = False
        self.live_thread_flag=False
        self.hcam.stopAcquisition()
        if self.ui.rcycles==0:
            self.lines.stop()
        self.ui.recordButton.setChecked(False)
        self.ui.recordButton.setText("record")
        self.ui.liveButton.setChecked(False)
        self.ui.liveButton.setText("live")
        try:
            self.tiff.close()#use libtiff
            #self.tiff.tinytiffclose(self.file)
        except:
            pass



    def stageUi(self):
        self.ui.message_label.setText('initializing stage Gui')
        self.stage = Stage.Stage()
        self.ui.message_label.setText('stage Gui initialized')


    def shutterUi(self):
        self.shutter = shutter.Shutter()


    def aotfUi(self):
        self.aotf = aotfui.Aotf()


    def galvoUi(self):
        self.galvo = Galvo.Galvo()

class Mythread(threading.Thread):
    def __init__(self,func):
        super().__init__()
        self.func=func

    def run(self):
        self.func()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = MainWindow()
    sys.exit(app.exec_())