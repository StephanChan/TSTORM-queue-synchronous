from PyQt5 import QtCore, QtGui, QtWidgets
import random

import numpy as np

import c_image_manipulation_c as c_image

class QtCameraGraphicsItem(QtWidgets.QGraphicsItem):
    def __init__(self,parent):
        super(QtCameraGraphicsItem, self).__init__()
        #self.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable)
        #self.setAcceptHoverEvents(True)
        self.chip_size_changed = False
        self.chip_x = 0
        self.chip_y = 0
        self.q_image=None
        self.test=0
        self.parent=parent
        #self.event=event



    def boundingRect(self):
        return QtCore.QRectF(0,0,600,600)


    def updateImageWithFrame(self, frame):
        """
        Convert the frame to a QImage, then call update() to display it.
        """
        #
        # For reasons lost in the mists of time 'frame' is a 1D numpy array
        # and needs to be reshaped before rescaling and converting to a QImage.
        #

        #image_data = frame.reshape((2048,2048))


        # Rescale the image & record it's minimum and maximum.
        '''[self.temp, self.image_min, self.image_max] = c_image.rescaleImage(frame,
                                                                      False,
                                                                      False,
                                                                      False,
                                                                      [0,255],
                                                                      None)
        # Create QImage & re-scale to compensate for binning, if any.
        temp_image = QtGui.QImage(self.temp.data, 2048, 2048, QtGui.QImage.Format_Indexed8)'''
        '''if (self.scale_x != 1) or (self.scale_y != 1):
            self.q_image = temp_image.scaled(w * self.scale_x, h * self.scale_y)
        else:
            self.q_image = temp_image
        self.q_image.ndarray = temp'''
        self.q_image = frame


        # Record the intensity where the user last clicked on the image.
        # self.click_x and self.click_y are in frame coordinates.
        #xl = self.click_x
        #yl = self.click_y
        '''if ((xl >= 0) and (xl < w) and (yl >= 0) and (yl < h)):
            self.intensity_info = image_data[yl, xl]
        else:
            self.intensity_info = 0'''

        # Force re-paint.
        self.parent.update()#you have to call scene's update() function instead of item's, cause in that way the update will fail to call paint after some time


    def paint(self, painter,option,widget):
            if self.q_image is None:
                print('no image come in')
                pass
                #painter.drawImage(0,0, QtGui.QImage("/home/nauge/PycharmProjects/TSTORM/practice/sv12.png"))
                #pixmap=QtGui.QImage("/home/nauge/PycharmProjects/TSTORM/practice/sv12.png")
                #painter.drawPixmap(0,0,QtGui.QPixmap.fromImage(pixmap))
                # Draw the grid into the buffer.
                '''if self.draw_grid:
                    x_step = self.chip_x / 8
                    y_step = self.chip_y / 8
                    painter.setPen(QtGui.QColor(255, 255, 255))
                    for i in range(7):
                        painter.drawLine((i + 1) * x_step, 0, (i + 1) * x_step, self.chip_y)
                        painter.drawLine(0, (i + 1) * y_step, self.chip_x, (i + 1) * y_step)
                # Draw the target into the buffer
                if self.draw_target:
                    mid_x = self.chip_x / 2 - 20
                    mid_y = self.chip_y / 2 - 20
                    painter.setPen(QtGui.QColor(255, 255, 255))
                    painter.drawEllipse(mid_x, mid_y, 40, 40)'''

            else:

                #pixmap01 = QtGui.QPixmap.fromImage(self.q_image)
                #painter.drawImage(100,100,self.q_image)
                #name="/home/nauge/PycharmProjects/TSTORM/practice/image/"+str(self.num)+'.png'
                #self.q_pix=QtGui.QPixmap.fromImage(self.q_image)

                painter.drawPixmap(QtCore.QRectF(0,0,600,600), self.q_image, QtCore.QRectF(0,0,600,600))
