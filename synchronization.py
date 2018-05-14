from PyDAQmx import *
import numpy as np
import ctypes
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import module
import time
import threading
import sys

class Lines(QWidget):
    signal=QtCore.pyqtSignal(float,float)
    def __init__(self,time_405=500,time_647=1000,frames=20,cycles=0,exposure=20):
        super().__init__()
        self.is_lines_runing = False
        self.read = np.int32()
        self.data = np.zeros(1, dtype=np.uint32)
        self.time_405=int(time_405)
        self.frames=int(frames)
        self.time_647=int(time_647)+12*self.frames
        self.cycles=int(cycles)
        self.exposure=int(exposure)+12
        self.done=bool32(0)


    def lists(self):
        self.list_405=[1]*self.time_405
        #self.list_405.extend([0]*self.frames*(self.exposure))



        self.list_647=[0]*self.time_405
        self.list_647.extend([1]*self.time_647)


        self.camera_list=[0]*self.time_405
        self.camera_list.extend(([1,1,1,1,1]+[0]*(self.exposure-5))*self.frames)

        max_=max(len(self.list_647),len(self.camera_list))
        self.list_405.extend([0]*(max_-len(self.list_405)))
        self.list_647.extend([0]*(max_-len(self.list_647)))
        self.camera_list.extend([0]*(max_-len(self.camera_list)))
        self.blk_list=[1]*max_


    def set_lines(self):
        self.task = Task()
        self.lists()
        self.task.CreateDOChan("/Dev1/port0/line1", "405", DAQmx_Val_ChanForAllLines)
        self.task.CreateDOChan("/Dev1/port0/line2", "647", DAQmx_Val_ChanForAllLines)
        self.task.CreateDOChan("/Dev1/port0/line3", "camera", DAQmx_Val_ChanForAllLines)
        self.task.CreateDOChan("/Dev1/port0/line4", "BLK", DAQmx_Val_ChanForAllLines)


        if self.cycles==0:
            self.task.CfgSampClkTiming("", 1000, DAQmx_Val_Rising, DAQmx_Val_ContSamps, 1000)

        else:
            self.list_405 *= self.cycles
            self.list_647 *= self.cycles
            self.camera_list *= self.cycles
            self.blk_list*=self.cycles
            self.list_405 +=[0,0]
            self.list_647 +=[0,0]
            self.camera_list +=[0,0]
            self.blk_list +=[0,0]
            self.task.CfgSampClkTiming("", 1000, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, len(self.list_405))

        data=[self.list_405,self.list_647,self.camera_list,self.blk_list]
        data=np.array(data,dtype=np.uint8)
        self.task.WriteDigitalLines(data.shape[1], 0, 10.0, DAQmx_Val_GroupByChannel, data, None,None)


    '''def start(self,n):
        if n>0:
            self.n=n
            #self.stop()
            #self.set_lines()
            print("lines is doing work %d"%n)
            #print("lines thread id : "+str(threading.current_thread()))
            self.task.StartTask()
            self.task.IsTaskDone(ctypes.byref(self.done))
            while( not self.done.value):
                time.sleep(1)
                self.task.IsTaskDone(ctypes.byref(self.done))
            self.stop()
            if self.is_lines_runing==True:
                self.signal.emit(self.n, self.stage_step)'''

    def run(self, step):

        self.task.StartTask()
        print("lines is doing work")
        #print("lines thread id : " + str(threading.current_thread()))
        self.task.IsTaskDone(ctypes.byref(self.done))
        while (not self.done.value):
            time.sleep(1)
            self.task.IsTaskDone(ctypes.byref(self.done))
        self.stop()

    def signal_emit(self):
        self.signal.emit(self.n, self.stage_step)



    def stop(self):
        self.task.StopTask()

    def clear(self):
        self.task.ClearTask()



if __name__=='__main__':
    app = QApplication(sys.argv)
    exa = Lines({})
    exa.set_lines()
    exa.start()
    sys.exit(app.exec_())