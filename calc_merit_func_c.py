import numpy as np
import random
import ctypes
from numpy.ctypeslib import ndpointer

class merit_func():
    def __init__(self):
        self.dll=ctypes.cdll.LoadLibrary('D:\storm-control-python3_pyqt5\storm-control-python3_pyqt5\storm_control\hal4000\my_hardware\\merit_func.dll')
        self.dll.merit_func.argtypes=[ndpointer(dtype=ctypes.c_double),
                                      ndpointer(dtype=ctypes.c_double),
                                      ctypes.c_int,
                                      ctypes.c_int,
                                      ctypes.POINTER(ctypes.c_double),
                                      ctypes.POINTER(ctypes.c_double)]

    def calc(self, image):
        merit_real=ctypes.c_double(0)
        merit_img=ctypes.c_double(0)
        image_fft=np.fft.fft2(image)
        image_real=image_fft.real
        size_x = ctypes.c_int(image.shape[1])
        size_y = ctypes.c_int(image.shape[0])
        image_img=image_fft.imag
        self.dll.merit_func(image_real,image_img,size_x,size_y,ctypes.pointer(merit_real),ctypes.pointer(merit_img))
        #merit_value=0+0j
        merit_value = merit_real
        merit_value.imag=merit_img

        merit_value/=np.sum(image_fft)
        return np.sqrt(merit_value.real**2+merit_value.imag**2)

if __name__=='__main__':
    import time
    test=merit_func()
    image=np.ones((2048*2048,),dtype=np.uint16)
    for i in range(2048*2048):
        image[i]=random.randint(0,65535)
    for i in range(100):
        start = time.clock()
        test.calc(image.reshape(2048, 2048)[768:1280,768:1280])
        stop = time.clock()
        print(stop - start)