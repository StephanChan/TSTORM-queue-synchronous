import ctypes
import numpy as np
from numpy.ctypeslib import ndpointer

class flmData(ctypes.Structure):
    _fields_=[('margin',ctypes.c_int),
              ('n_peaks',ctypes.c_int),
              ('radius',ctypes.c_int),
              ('xsize',ctypes.c_int),
              ('ysize',ctypes.c_int),
              ('threshold',ctypes.c_double),
              ('taken',ctypes.POINTER(ctypes.c_int)),
              ('image',ndpointer(dtype=ctypes.c_int16))]

finder=ctypes.cdll.LoadLibrary('dll_path')
finder.findLocalMaxima.argtypes = [ctypes.POINTER(flmData),
                                   ctypes.POINTER(ctypes.c_int),
                                   ctypes.POINTER(ctypes.c_int),
                                   ctypes.POINTER(ctypes.c_int)]

finder.findLocalMaxima.restype=ctypes.c_int

class peak_counter:
    def __init__(self):
        self.flmData=flmData()
        self.flmData.margin=ctypes.c_int(0)
        self.flmData.n_peaks=ctypes.c_int(10000)
        self.flmData.radius=ctypes.c_int(8)

    def set_flmData(self,image):
        self.flmData.xsize=ctypes.c_int(image.shape[0])
        self.flmData.ysize=ctypes.c_int(image.shape[1])
        self.flmData.threshold=ctypes.c_double(170.0)
        self.flmData.taken=(ctypes.c_int*(self.flmData.ysize*self.flmData.xsize))()
        self.image=image

    def find_peaks(self):
        x=(ctypes.c_int*self.flmData.n_peaks)()
        y=(ctypes.c_int*self.flmData.n_peaks)()
        h=(ctypes.c_int*self.flmData.n_peaks)()
        return finder.findLocalMaxima(ctypes.pointer(self.flmData),x,y,h)


if __name__=='__main__':
    image=np.zeros((12,12))
    my_peaks=peak_counter()
    my_peaks.set_flmData(image)
    print(my_peaks.flmData.taken[100])
    print(my_peaks.flmData.image)
