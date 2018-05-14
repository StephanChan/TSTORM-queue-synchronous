import ctypes
import random
from numpy.ctypeslib import ndpointer
import numpy as np
import time

class DMirror(object):
    dll_loaded=False
    def __init__(self,dll_path):
        super().__init__()
        self.status=ctypes.c_int(0)
        self.dm=None
        if not DMirror.dll_loaded:
            self.loadDMDLL(dll_path)
            DMirror.dll_loaded = True
            self.mro_open=getattr(self.dm,'mro_open')
            self.mro_close=getattr(self.dm,'mro_close')
            self.mro_applySmoothCommand=getattr(self.dm,'mro_applySmoothCommand')
            self.mro_readfile=getattr(self.dm,'mro_readCommandFile')
            self.mro_open.argtypes=[ctypes.POINTER(ctypes.c_int)]
            self.mro_close.argtypes=[ctypes.POINTER(ctypes.c_int)]

            self.mro_applySmoothCommand.argtypes=[ndpointer(dtype=ctypes.c_double),
                                                ctypes.c_char,
                                                     ctypes.POINTER(ctypes.c_int)]
            self.mro_readfile.argtypes=[ctypes.POINTER(ctypes.c_char),
                                        ndpointer(dtype=ctypes.c_double),
                                        ctypes.POINTER(ctypes.c_int)]

    def loadDMDLL(self,dll_path):
        """
        Handles loading the library (only once).
        """
        if self.dm is None:
            self.dm = ctypes.windll.LoadLibrary(dll_path)

    def DM_open(self):
        if DMirror.dll_loaded == True:

            if self.mro_open(ctypes.pointer(self.status))==0:
                print('status: ',self.status)

    def DM_close(self):
        if DMirror.dll_loaded == True:
            if self.mro_close(ctypes.pointer(self.status))==0:
                print('status: ',self.status)

    def DM_applySmoothCommand(self,command,trig=b'0'):
        if DMirror.dll_loaded == True:
            if self.mro_applySmoothCommand(command,trig,ctypes.pointer(self.status))==0:
                print('status: ',self.status)

    def DM_read_file(self,command,path):
        if DMirror.dll_loaded == True:
            if self.mro_readfile(path,command,ctypes.pointer(self.status))==0:
                print('status: ',self.status)


if __name__=='__main__':
    dm_handle=DMirror('C:\\Program Files (x86)\\Imagine Optic\\WaveTune\\dlls\\mirao52e.dll')
    dm_handle.DM_open()
    command=[0]*52
    for i in range(len(command)):
        command[i]=random.random()/4
    for i in range(100):
        if i%2==0:
            dm_handle.DM_applySmoothCommand(np.array(command))
        else:

            dm_handle.DM_applySmoothCommand(-np.array(command))
        time.sleep(1)
    dm_handle.DM_close()