import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QBrush
import threading
import random
import numpy as np
import datetime
import time as Time

class picture(QLabel):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.resize(400,400)
        self.delta=self.width()/6
        self.delta_x=self.width()/100
        self.y_max=14.0
        self.x=[]
        self.y=[]
        self.func=[]
        self.path='/home/nauge/PycharmProjects/TSTORM/practice/image/'
        self.mode_name=''


    '''def paintEvent(self,event):
        qp = QPainter(self)
        qp.drawPixmap(0,0,self.q_pixmap)
        qp.setPen(QColor(255,255,255))
        for i in range(len(self.x)):
            qp.drawPoint(self.x[i],
                         self.y[i])'''
    def paintEvent(self,event):
        image=QtGui.QImage(400,400,QtGui.QImage.Format_RGB32)
        qp=QPainter(image)
        color=QtGui.QColor(255,255,255)
        qp.setPen(color)
        qp.setBrush(color)
        qp.drawRect(0,0,self.width(),self.height())

        qp.setPen(QtGui.QColor(0,255,0))
        qp.setBrush(QtGui.QColor(0,255,0))
        for i in range(len(self.x)):
            x=int(self.delta*i)
            y=self.height()-int(self.y[i]/self.y_max*self.height())
            qp.drawEllipse(x-2,y-2,4,4)

        qp.setPen(QtGui.QColor(255,0,0))
        qp.setBrush(QtGui.QColor(255,0,0))
        for i in range(len(self.func)):
            x = int(self.delta_x * i)
            y = self.height() - int(self.func[i] / self.y_max * self.height())
            qp.drawEllipse(x-1,y-1,2,2)
        qp.end()
        time = datetime.datetime.now()
        image.save(self.path+self.mode_name+'-'+str(time)[11:13]+'-'+str(time)[14:16]+'_'+str(time)[17:19]+'.png','PNG')
        p=QPainter(self)
        p.drawPixmap(self.rect(), QtGui.QPixmap(image))
        p.end()

    def update_peaks(self,x,y,func,mode_name):
        self.x=np.array(x)
        self.y=np.array(y)
        self.func=np.array(func)
        self.mode_name=mode_name
        self.update()

class display(QWidget):

    def __init__(self):
        super().__init__()

        self.lb = picture(self)

        self.setWindowTitle('peaks')
        self.setGeometry(300,300,400,400)
        #self.a_thread()
        self.show()

    def a_thread(self):
        a_thread=threading.Thread(target=self.test)
        a_thread.start()

    def test(self):
        for i in range(105):
            x=[]
            y=[]
            #func=[]
            for i in range(5):
                x += [random.randint(0, 5)]
                y += [random.randint(0, 14)]
            func=[i for i in fun() if i>0]
            self.lb.update_peaks(x, y, func, 'a_mode')
            Time.sleep(0.4)
def fun():
    x=np.arange(0,2,0.02)
    return 14*(x-1)**2-1

if __name__=='__main__':
    app = QApplication(sys.argv)
    window = display()
    sys.exit(app.exec_())