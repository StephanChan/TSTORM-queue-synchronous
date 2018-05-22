import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QBrush
import threading
import random
import numpy as np
import time

class picture(QLabel):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.resize(400,400)
        self.q_pixmap = QtGui.QPixmap(400, 400)
        self.x=[]
        self.y=[]



    def paintEvent(self,event):
        qp = QPainter(self)
        qp.drawPixmap(0,0,self.q_pixmap)
        qp.setPen(QColor(255,255,255))
        for i in range(len(self.x)):
            qp.drawPoint(self.x[i],
                         self.y[i])

    def update_peaks(self,x,y):
        self.x=np.array(x)/2048.0*400
        self.y=np.array(y)/2048.0*400
        self.update()


class SpotGraph(QLabel):
    """
    The spot graph for a camera feed.
    """

    def __init__(self, parent):
        super().__init__(parent=parent)

        self.x_points = 100
        self.y_max = 500.0
        self.resize(300, 300)
        self.colors=[None]
        self.data=[]
        self.cycle_length=1

        self.delta_x = float(self.width()) / float(self.x_points - 1)
        self.delta_y = float(self.height()) / 5.0

    def clearGraph(self):
        self.data = np.zeros(self.x_points, dtype=np.uint16)
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        # White background.
        color = QtGui.QColor(255, 255, 255)
        painter.setPen(color)
        painter.setBrush(color)
        painter.drawRect(0, 0, self.width(), self.height())

        #
        # Grid Lines.
        #
        # Draw lines in y to denote the start of each cycle, but only
        # if we have at least 2 points per cycle.
        #
        # Draw grid lines in x.
        #
        painter.setPen(QtGui.QColor(200, 200, 200))
        if (self.cycle_length > 1):
            x = 0.0
            while x < float(self.width()):
                ix = int(x)
                painter.drawLine(ix, 0, ix, self.height())
                x += self.delta_x * self.cycle_length

        y = 0.0
        while y < float(self.height()):
            iy = int(y)
            painter.drawLine(0, iy, self.width(), iy)

            y += self.delta_y

        #
        # Plot the data.
        #

        # Lines
        '''painter.setPen(QtGui.QColor(0, 0, 0))
        x1 = 0
        y1 = self.height() - int(self.data[0] / self.y_max * self.height())
        for i in range(self.data.size - 1):
            x2 = int(self.delta_x * float(i + 1))
            y2 = self.height() - int(self.data[i + 1] / self.y_max * self.height())
            painter.drawLine(x1, y1, x2, y2)
            x1 = x2
            y1 = y2'''

        # Points
        for i in range(len(self.data)):
            color = self.colors[i % self.cycle_length]
            if color is None:
                qt_color = QtGui.QColor(255, 255, 255)
            else:
                qt_color = QtGui.QColor(*color)
            painter.setPen(QtGui.QColor(0, 0, 0))
            painter.setBrush(qt_color)

            x = int(self.delta_x * float(i))
            y = self.height() - int(self.data[i] / self.y_max * self.height())
            painter.drawEllipse(x - 2, y - 2, 4, 4)

    def resizeEvent(self, event):
        self.delta_x = float(self.width()) / float(self.x_points - 1)
        self.delta_y = float(self.height()) / 5.0
        self.update()

    def setMaxSpots(self, max_spots):
        self.y_max = float(max_spots)
        self.update()

    def updatePoint(self, counts):
        if len(self.data)==100:
           self.data=self.data[1:]
        self.data+=[counts]
        self.update()



class spotpicture(QWidget):

    def __init__(self):
        super().__init__()

        self.lb = picture(self)

        self.setWindowTitle('peaks')
        self.setGeometry(300,300,400,400)
        self.a_thread()
        self.show()

    def a_thread(self):
        a_thread=threading.Thread(target=self.test)
        a_thread.start()

    def test(self):
        for i in range(105):
            x=[]
            y=[]
            for i in range(100):
                x += [random.randint(0, 2048)]
                y += [random.randint(0, 2048)]
            self.lb.update_peaks(x, y)
            time.sleep(0.4)


class spotgraph(QWidget):
    def __init__(self):
        super().__init__()
        self.lb=SpotGraph(self)
        self.setWindowTitle('counts')
        self.setGeometry(300,300,300,300)

        self.a_thread()
        self.show()

    def a_thread(self):
        a_thread=threading.Thread(target=self.test)
        a_thread.start()

    def test(self):
        for i in range(105):
            count = random.randint(0, 500)
            self.lb.updatePoint(count)
            time.sleep(0.5)

if __name__ == '__main__':
    import time
    app = QApplication(sys.argv)
    ex = spotpicture()

    sys.exit(app.exec_())