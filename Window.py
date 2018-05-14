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
import peak_finder_c as counter
import DM
import tinytiffwriter
import tifffile
import libtiff


class MainWindow(QtCore.QObject):
    stop_record_signal = QtCore.pyqtSignal()#init signal
    def __init__(self):
        super().__init__()
        self.ui=ui.MainWindow()
        self.ui.setupMainWindow()
        self.ui.show()
        self.dm=None
        self.queue = Queue()#init queue that will contain synchronous recording actions
        self.frames = []
        self.lines = None
        self.live_thread_flag = None
        self.record_thread_flag = None
        self.filepath = 'D:\\Data\\'
        self.filename = None
        self.rescale_min = 0
        self.rescale_max = 65535
        self.lock = threading.Lock()#lock used to protect codes from multi threads
        self.hcam = cam.HamamatsuCameraMR(camera_id=0)#camera handle
#connect button to functions
        self.ui.shutterButton.clicked.connect(lambda: self.shutterUi())
        self.ui.AOTFButton.clicked.connect(lambda: self.aotfUi())
        self.ui.GalvoButton.clicked.connect(lambda: self.galvoUi())
        self.ui.StageButton.clicked.connect(lambda: self.stageUi())
        self.ui.DMButton.clicked.connect(lambda: self.DMUi())
        self.ui.liveButton.clicked.connect(lambda: self.live_state_change())
        self.ui.one_record_button.clicked.connect(lambda: self.record_one_frame_thread())
        self.ui.recordButton.clicked.connect(lambda: self.record_state_change())
        self.ui.IrecordButton.clicked.connect(lambda: self.Irecord_state_change())
        self.ui.autoscalebutton.clicked.connect(lambda: self.autoscale())
        self.ui.slider_up.valueChanged.connect(lambda: self.upscale())
        self.ui.slider_down.valueChanged.connect(lambda: self.downscale())
        self.ui.livewindow.click_on_pixel.connect(self.getIntensityInfo)
        self.ui.set_expo.clicked.connect(lambda: self.set_expo())
        self.ui.set_record_expo.clicked.connect(lambda: self.set_record_expo)
        self.stop_record_signal.connect(lambda: self.stop_record())

        self.live_thread = threading.Thread(target=self.display, name='liveThread')
        self.record_thread = threading.Thread(target=self.recording, name="recordThread")


    def getIntensityInfo(self,x,y):
#put pixel grey level value on message_label
        self.ui.message_label.setText('pixel grey level:'+str(self.frames[0][2048*y+x]))
        #self.ui.message_label.setText('pixel grey level:' + str(x)+'   '+str(y))

    def autoscale(self):
        #for all pixels in image, if pixel value <self.rescale_min, pixel value =0
        #for all pixels in image, if pixel value> self.rescale_max, pixel value=255
        #self.image_min, self.image_max is the minimum and maximum pixel value in precceding image
        try:
            self.rescale_min = self.image_min
            self.rescale_max = self.image_max
        except:
            print("not start display yet")

#manually adjust the rescale_max
    def upscale(self):
        self.rescale_max=self.ui.slider_up.value()

#manually adjust the rescale_min
    def downscale(self):
        self.rescale_min=self.ui.slider_down.value()

#set camera exposure in living
    def set_expo(self):
        self.hcam.setPropertyValue('exposure_time', float(self.ui.cam_expo.text())/1000.0)

#set camera exposure in isolated recording
    def set_record_expo(self):
        self.hcam.setPropertyValue('exposure_time', float(self.ui.Icam_expo.text())/1000.0)

#this is the function that get image from camera buffer and unblock live/record threads is flag is True
    def get_buffer(self,event_live,event_record):
            [self.frames, dims] = self.hcam.getFrames()
            #print('frames: '+str(len(self.frames)))
            #print(str(len(self.frames)) + "  frames get")
            if self.live_thread_flag == True:
                event_live.set()#unblock live thread
                if not self.live_thread.is_alive() :#sometimes live thread exits when is should not, then restart live thread
                    self.live_thread = threading.Thread(target=self.display, args=(self.event_live,), name='liveThread')
                    self.live_thread.start()


            if self.record_thread_flag == True:
                event_record.set()#unblock record thread



#this is the buffer_thread, calls get_buffer function every 0.13 second
    def buffer_thread(self,event_live,event_record):
        while(self.live_thread_flag==True):
            #start = time.clock()
            time.sleep(0.15)
            self.get_buffer(event_live,event_record)
            #stop = time.clock()
            #print('time: ',stop-start)

#when live button is clicked, call this function
    def live_state_change(self):
            if self.ui.liveButton.isChecked():
                try:#if synchronous recording is executed before this action, first disconnect the connection
                    self.disconnect()
                except:
                    pass

                self.start_living()
            else:
                self.stop_living()


    def start_living(self):
        self.ui.liveButton.setText('stop live')
        self.live_thread_flag = True
        self.hcam.startAcquisition()#set camera state can be triggered to exposure
        self.hcam.setPropertyValue('exposure_time', float(self.ui.cam_expo.text()) / 1000.0)
        self.event_live=threading.Event()#init event which is used to block threads
        self.event_record=threading.Event()
        #init get_buffer thread
        self.get_buffer_thread = threading.Thread(target=self.buffer_thread, args=(self.event_live,self.event_record), name='buffer thread')
        self.get_buffer_thread.start()
        #init live thread. live thread and get_buffer thread are always together, i.e., both alive or both dead
        self.live_thread = threading.Thread(target=self.display, args=(self.event_live,), name='liveThread')
        self.live_thread.start()
        self.event_peak_count=threading.Event()
        #self.peak_count_thread=threading.Thread(target=self.peak_count, args=(self.event_peak_count,),name='peak count thread')
        #self.peak_count_thread.start()


    def stop_living(self):
        self.live_thread_flag = False
        #self.event_live.clear()
        self.hcam.stopAcquisition()#set camera state cannot be triggered
        self.ui.liveButton.setText('Live')

    def peak_count(self,event):
        self.counter = counter.peak_counter()
        while(self.live_thread_flag==True):
            event.wait(1)
            event.clear()
            self.counter.set_flmData(self.image,np.zeros((2048*2048,),dtype=ctypes.c_int))
            num=self.counter.find_peaks()
            self.ui.label_counts.setText(str(num))


#this is the live thread that display image on main window
    def display(self,event):
        '''live child thread
                    display images when one cycle ends'''
        # pid = os.getpid()
        # print("living PID: " + str(pid))
        # print("living thread id: "+str(threading.current_thread().name))
        while (self.live_thread_flag == True):
            event.wait(1)#block the thread, unless get_buffer function unblocks it or after 1 second it automatically unblock itself
            event.clear()#recover the event to blockable
            try:
                self.image = self.frames[0].np_array.reshape((2048, 2048))#reshape the array from 1d array to 2048*2048 array
                #print(type(self.image[0][0]))
                #self.event_peak_count.set()
                if self.dm and self.dm.ui.on_button.isChecked():
                    self.dm.image_update(self.image)
            except:
                return 0

            self.lock.acquire()#bellow codes are protected
            rescale_min = self.rescale_min
            rescale_max = self.rescale_max
            #c function that transfers image data type from 16 bit to 8 bit and returns the minimum and maximum value in the image
            [temp, self.image_min, self.image_max] = c_image.rescaleImage(self.image,
                                                                          False,
                                                                          False,
                                                                          False,
                                                                          [rescale_min, rescale_max],
                                                                          None)
            self.lock.release()#lock stops here
            self.ui.max_label.setText(str(self.image_max))#show image maximum value on the main window
            self.ui.min_label.setText(str(self.image_min))
            qImg = QtGui.QImage(temp.data,2048, 2048, QtGui.QImage.Format_Indexed8)#change data type from ndarray to QImage
            pixmap01 = QtGui.QPixmap.fromImage(qImg)#change data type from QImage to QPixmap
            #self.ui.livewindow.setPixmap(pixmap01)
            self.ui.item.updateImageWithFrame(pixmap01)#call updateImageWithFrame function to update image on the main window
            #print('living')
        print('live thread exits')#FIXME: why this sentence is not processed



            # stop=time.clock()
            # print("time for one frame display: "+str(stop-start))
    def record_one_frame_thread(self):
        one_frame_thread=threading.Thread(target=self.record_one_frame, name='one_frame_thread')
        one_frame_thread.start()

    def record_one_frame(self):
        image=self.frames[0]
        if self.ui.name_text.text() == 'name your file':
            time = datetime.datetime.now()  # get current time
            self.filename = self.filepath + str(time)[:10] + '_' + str(time)[11:13] + '_' + str(time)[
                                                                                            14:16]  # name file after current time
        else:
            self.filename = self.filepath + self.ui.name_text.text() + '_' + self.ui.name_num.text()
        # choose file type, tiff or dax
        if self.ui.file_type.currentText() == '.tif':
            # self.file = libtiff.TIFF.open(self.filename + '.tif', mode='w8')
            self.file = tifffile.TiffWriter(self.filename + '.tif', bigtiff=True)
        else:
            self.file = DaxFile(self.filename)
        if self.ui.file_type.currentText() == '.tif':
            image = image.np_array.reshape((2048, 2048))
            # self.file.write_image(image)#write image to tiff file
            self.file.save(image)  # tifffile
        else:
            self.file.write_image(image)  # write image to dax file
            # self.tiff.tinytiffwrite(image,self.file)


    # when record button is clicked, set record flag to True or False, then record thread will start or stop
    def Irecord_state_change(self):
        if not self.ui.IrecordButton.isChecked():#stop recording
            self.ui.IrecordButton.setText('isolated record')
            self.stop_record()

        else:#start recording
            if not self.ui.liveButton.isChecked():#if live thread is dead, start live thread
                self.ui.liveButton.setChecked(True)
                self.live_state_change()
            time = datetime.datetime.now()#get current time
            #self.filename = self.filepath + str(time)[:10] + '_' + str(time)[11:13] + '_' + str(time)[
            #                                                                                14:16]  # name file after current time
            if self.ui.name_text.text() == 'name your file':
                self.filename = self.filepath + str(time)[:10] + '_' +str(time)[11:13]+'_'+str(time)[14:16]#name file after current time
            else:
                self.filename= self.filepath + self.ui.name_text.text()+'_'+self.ui.name_num.text()
            #choose file type, tiff or dax
            if self.ui.file_type.currentText()=='.tif':
                #self.file = libtiff.TIFF.open(self.filename + '.tif', mode='w8')
                self.file=tifffile.TiffWriter(self.filename+ '.tif',bigtiff=True)
            else:
                self.file = DaxFile(self.filename)
            self.record_thread_flag = True
            #init recording thread
            self.record_thread = threading.Thread(target=self.recording, args=(self.event_record,), name="recordThread")
            self.record_thread.start()
            self.ui.IrecordButton.setText('stop')
            self.hcam.setPropertyValue('exposure_time', float(self.ui.Icam_expo.text())/1000.0)

#when synchronous record button is clicked, call this function
    def record_state_change(self):
        if not self.ui.recordButton.isChecked():
            self.stop_record()
        else:
            self.connect()#connect the AOTF to external trigger

            self.start_record()



    def disconnect(self):#disconnect AOTF to external trigger
        self.hcam.setPropertyValue("trigger_source", 1)
        self.aotf.ui.button_analog.setChecked(False)
        self.aotf.analog()


    def connect(self):

        self.hcam.setPropertyValue("trigger_source", 2)
        self.hcam.setPropertyValue("trigger_active", 1)
        self.aotf.ui.button_analog.setChecked(True)
        #self.aotf.ui.textbox_a1.setText('25')
        self.aotf.analog()
        #init digital signal
        self.lines=syn.Lines(time_405=float(self.ui.r_405_expo.text()),time_647=float(self.ui.r_647_expo.text()),
                                   frames=float(self.ui.rframes.text()),
                             cycles=float(self.ui.rcycles.text()),exposure=float(self.ui.rcam_expo.text()))

#this is the record thread
    def recording(self,event):
        '''record child thread
        record frames when one cycle ends'''

        #print("record thread id: " + str(threading.current_thread()))
        self.num=0
        count=0
        while(self.record_thread_flag==True):
            event.wait(1)#block record thread unless get_buffer unblocks it or after 1 second it unblocks itself
            event.clear()#set event to blockable
            #start = time.clock()
            for num,image in enumerate(self.frames):
                #print(num, len(self.frames))
                self.num+=1#count image numbers
                if self.num>=800:#maximum image number in a file is 800, when image exceeds this number, close current file and open another one
                    count+=1#used to name subsequent files
                    if self.ui.file_type.currentText() == '.tif':
                        self.file.close()
                        #open another file
                        self.file = tifffile.TiffWriter(self.filename +'-'+str(count)+ '.tif',bigtiff=True)
                    else:
                        self.file.close(self.num)
                        self.file = DaxFile(self.filename+'-'+str(count))
                    self.num=1#reinit image number
                if self.ui.file_type.currentText() == '.tif':
                    image = image.np_array.reshape((2048, 2048))
                    #self.file.write_image(image)#write image to tiff file
                    self.file.save(image)#tifffile
                else:
                    self.file.write_image(image)#write image to dax file
                # self.tiff.tinytiffwrite(image,self.file)
                # tifffile.imsave(self.filename, image) #use tifffile.py
            #stop=time.clock()
            #print('time used" ',stop-start)
        print('record thread exits')


#before synchronous recording, set all the parameters, say, file name
    def start_record(self):
        self.lines.set_lines()
        #self.tiff = tinytiffwriter.tinytiffwriter()#use tinytiffwriter.dll
        #self.file = self.tiff.tinytiffopen(self.filename,16,2048,2048)
        time = datetime.datetime.now()
        if self.ui.name_text.text() == 'name your file':
            self.filename = self.filepath + str(time)[:10] + '_' + str(time)[11:13] + '_' + str(time)[
                                                                                            14:16]  # name file after current time
        else:
            self.filename = self.filepath + self.ui.name_text.text() + '-' + self.ui.name_num.text()

        if self.ui.file_type.currentText() == '.tif':
            self.file = tifffile.TiffWriter(self.filename + '.tif', bigtiff=True)
        else:
            self.file = DaxFile(self.filename)

        self.record_thread_flag = True
        self.live_thread_flag=True
        self.ui.recordButton.setText('stop')
        self.hcam.setPropertyValue('exposure_time', float(self.ui.rcam_expo.text()) / 1000.0)
        for i in range(int(float(self.ui.range.text()) / float(self.ui.step.text()))):
            self.in_queue()#put actions into queue, say, stage move and digital signal for AOTF

        self.synchronous_thread = Mythread(self.worker)#open another thread used for synchronous action
        self.record_thread = threading.Thread(target=self.recording, args=(self.event_record,), name="recordThread")
        if not self.live_thread.is_alive():
            self.live_thread = threading.Thread(target=self.display, args=(self.event_live,), name='liveThread')
            self.live_thread.start()

        self.record_thread.start()
        self.synchronous_thread.start()


#function that put actions into queue
    def in_queue(self):
        self.queue.put({'lines': 0})
        self.queue.put({'stage': float(self.ui.step.text())})

#parameter for class Mythread, get action from queue and execute action
    def worker(self):
        while not self.queue.empty():
            if self.record_thread_flag==True:
                item = self.queue.get()
                module = getattr(self, str(list(item.keys())[0]))
                module.run(item[str(list(item.keys())[0])])
                #time.sleep(0.1)
            else:
                break
#when all the actions are executed and the queue is empty, it means synchronous recording finishs, call stop_record()
        self.stop_record()

    def stop_record(self):
        #self.event_live.clear()
        #self.event_record.clear()
        self.record_thread_flag = False
        self.live_thread_flag=False
        self.hcam.stopAcquisition()
        if self.ui.rcycles==0:#if it's isolated record mode, the digital signal has to be manually stopped
            self.lines.stop()
        self.ui.recordButton.setChecked(False)
        self.ui.recordButton.setText("record")
        self.ui.liveButton.setChecked(False)
        self.ui.liveButton.setText("live")
        #close file
        if self.ui.file_type.currentText() == '.tif':
            time.sleep(0.1)
            self.file.close()
            time.sleep(0.1)
        else:
            self.file.close(self.num)
            # self.tiff.tinytiffclose(self.file)



#stage handle
    def stageUi(self):
        self.ui.message_label.setText('initializing stage Gui')
        self.stage = Stage.Stage()
        self.ui.message_label.setText('stage Gui initialized')

#shutter handle
    def shutterUi(self):
        self.shutter = shutter.Shutter()

#AOTF handle
    def aotfUi(self):
        self.aotf = aotfui.Aotf()

#Galvo handle
    def galvoUi(self):
        self.galvo = Galvo.Galvo()

    def DMUi(self):
        self.dm=DM.remove_aberration()

#class that customize thread in synchronous record
class Mythread(threading.Thread):
    def __init__(self,func):
        super().__init__()
        self.func=func

    def run(self):
        self.func()

#class that write dax file
class DaxFile():
    """
    Dax file writing class.
    """
    def __init__(self,filename, **kwds):
        super().__init__(**kwds)
        self.filename=filename+'.dax'
        self.basename=filename
        self.fp = open(self.filename, "wb")

    def close(self,num):
        """
        Close the file and write a very simple .inf file. All the metadata is
        now stored in the .xml file that is saved with each recording.
        """
        self.fp.close()
        with open(self.basename + ".inf", "w") as inf_fp:#write info file
            inf_fp.write("binning = 1 x 1\n")
            inf_fp.write("data type = 16 bit integers (binary, little endian)\n")
            inf_fp.write("frame dimensions = " + str(2048) + " x " + str(2048) + "\n")
            inf_fp.write("number of frames = " + str(num) + "\n")
            if True:
                inf_fp.write("x_start = 1\n")
                inf_fp.write("x_end = " + str(2048) + "\n")
                inf_fp.write("y_start = 1\n")
                inf_fp.write("y_end = " + str(2048) + "\n")
            inf_fp.close()

    def write_image(self, frame):
        np_data = frame.getData()
        np_data.tofile(self.fp)#write image to dax file

if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = MainWindow()
    sys.exit(app.exec_())