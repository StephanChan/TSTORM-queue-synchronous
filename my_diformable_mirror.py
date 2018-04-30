import ctypes
import random
from numpy.ctypeslib import ndpointer

class DMirror(object):
    dll_loaded=False
    def __init__(self,dll_path):
        super().__init__()
        self.status=ctypes.c_int(0)
        self.dm=None
        if not DMirror.dll_loaded:
            self.loadDMDLL(dll_path)
            DMirror.dll_loaded = True
            self.dm.mro_open.argtypes=[ctypes.POINTER(ctypes.c_int)]
            self.dm.mro_close.argtypes=[ctypes.POINTER(ctypes.c_int)]
            self.dm.mro_applySmoothCommand.argtypes=[ndpointer(dtype=ctypes.c_double),
                                                ctypes.c_char,
                                                     ctypes.POINTER(ctypes.c_int)]

    def loadDMDLL(self,dll_path):
        """
        Handles loading the library (only once).
        """
        if self.dm is None:
            self.dm = ctypes.cdll.LoadLibrary(dll_path)

    def DM_open(self):
        if DMirror.dll_loaded == True:
            if self.dm.mro_open(ctypes.pointer(self.status))==0:
                print('status: ',self.status)

    def DM_close(self):
        if DMirror.dll_loaded == True:
            if self.dm.mro_close(ctypes.pointer(self.status))==0:
                print('status: ',self.status)

    def DM_applySmoothCommand(self,command,trig='0'):
        if DMirror.dll_loaded == True:
            if self.dm.mro_applySmoothCommand(command,trig,ctypes.pointer(self.status))==0:
                print('status: ',self.status)

if __name__=='__main__':
    dm_handle=DMirror('dll_path')
    dm_handle.DM_open()
    command=[0]*52
    for i in range(len(command)):
        command[i]=random.random()/4
    dm_handle.DM_applySmoothCommand(command)
    dm_handle.DM_close()
