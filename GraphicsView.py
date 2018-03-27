from PyQt5 import QtCore, QtGui, QtWidgets


class QtCameraGraphicsView(QtWidgets.QGraphicsView):
    #dragMove = QtCore.pyqtSignal(int, int)
    #dragStart = QtCore.pyqtSignal()
    #newCenter = QtCore.pyqtSignal(int, int)
    #newScale = QtCore.pyqtSignal(int)
    click_on_pixel=QtCore.pyqtSignal(int,int)

    def __init__(self):
        super(QtCameraGraphicsView,self).__init__()
        self.can_drag = False
        self.chip_max = 100
        self.center_x = 0
        self.center_y = 0
        self.ctrl_key_down = False
        self.display_scale = 0.5
        self.drag_mode = False
        self.drag_x = 0
        self.drag_y = 0
        self.frame_size = 0
        self.max_scale = 8
        self.min_scale = -8
        self.transform = QtGui.QTransform()
        self.viewport_min = 100

        #self.newCenter.connect(lambda: self.getCurrentCenter(1,1))


    '''def getCurrentCenter(self,x,y):
        center = self.mapToScene(self.viewport().rect().center())
        self.center_x = center.x()
        self.center_y = center.y()
        self.newCenter.emit(self.center_x, self.center_y)
        #print('current center: ',self.center_x,self.center_y)'''



    '''def mouseMoveEvent(self, event):

        #print(self.point.x(),self.point.y())
        if self.drag_mode:
            self.dragMove.emit(event.x() - self.drag_x,
                               event.y() - self.drag_y)
        else:
            super().mouseMoveEvent(event)'''

    '''def calcScale(self, size):
        if (size < self.viewport_min):
            return int(self.viewport_min/size) -1
        else:
            return -int(size/self.viewport_min)'''

    '''def enableStageDrag(self, enabled):
        self.can_drag = enabled'''

    '''def keyPressEvent(self, event):
        if self.can_drag and (event.key() == QtCore.Qt.Key_Control):
            self.ctrl_key_down = True
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def keyReleaseEvent(self, event):
        if self.can_drag and (event.key() == QtCore.Qt.Key_Control):
            self.ctrl_key_down = False
            self.drag_mode = False
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))'''

    def mousePressEvent(self, event):
        pos = self.mapToScene(event.pos())
        #self.center_x = pos.x()
        #self.center_y = pos.y()
        #self.newCenter.emit(self.center_x, self.center_y)
        #self.centerOn(self.center_x, self.center_y)
        #self.point = QtCore.QPointF(self.mapToScene(event.globalPos()))
        self.click_on_pixel.emit(pos.x(),pos.y())

        '''if self.ctrl_key_down:
            self.drag_mode = True
            self.drag_x = event.x()
            self.drag_y = event.y()
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            self.dragStart.emit()
        else:
            super().mousePressEvent(event)'''
        super().mousePressEvent(event)

    '''def mouseReleaseEvent(self, event):
        if self.drag_mode:
            self.drag_mode = False
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        else:
            super().mouseReleaseEvent(event)'''

    '''def resizeEvent(self, event):
        #
        # Use the GraphicsView contentsRect size and not it's viewport
        # contentsRect size because depending on the zoom scroll bars
        # will appear and disappear throwing off the calculation.
        #
        # viewport_rect = self.viewport().contentsRect()
        viewport_rect = self.contentsRect()
        self.viewport_min = viewport_rect.width() if (viewport_rect.width() < viewport_rect.height()) \
            else viewport_rect.height()

        self.min_scale = self.calcScale(self.chip_max)
        if (self.display_scale < self.min_scale):
            self.display_scale = self.min_scale

        super().resizeEvent(event)'''

    def rescale(self, scale):
        """
        Rescale the view so that it looks like we have zoomed in/out.

        """

        if (scale < self.min_scale) or (scale > self.max_scale):
            return

        self.display_scale = scale
        #self.newScale.emit(self.display_scale)

        if (self.display_scale == 0):
            flt_scale = 1.0
        elif (self.display_scale > 0):
            flt_scale = float(self.display_scale *1.01)
        else:
            flt_scale = 1.0 / (-self.display_scale +1)

        transform = QtGui.QTransform()
        transform.scale(flt_scale, flt_scale)
        self.setTransform(self.transform * transform)
        self.centerOn(self.center_x,self.center_y)

    def wheelEvent(self, event):
        """
        Zoom in/out with the mouse wheel.
        """
        if not event.angleDelta().isNull():
            if (event.angleDelta().y() > 0):
                self.rescale(self.display_scale+0.1)
            else:
                self.rescale(self.display_scale - 0.1)
            event.accept()
        #print(self.display_scale)
