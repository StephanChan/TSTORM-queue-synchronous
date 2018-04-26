import ctypes
from numpy.ctypeslib import ndpointer

dm=None
def loadDMDLL(dm_dll):
    """
    Handles loading the library (only once).
    """
    global dm
    if dm is None:
        dm = ctypes.cdll.LoadLibrary(dm_dll)

class DMirror(object):
    dll_loaded=False
    handle_grabbed=False
    def __init__(self,dm_dll):
        super().__init__()
        self.status=0
        if not DMirror.dll_loaded:
            loadDMDLL(dm_dll)
            DMirror.dll_loaded = True
            dm.mro_open.argtypes=[ndpointer(dtype=ctypes.c_int)]
            dm.mro_close.argtypes=[ndpointer(dtype=ctypes.c_int)]
            dm.mro_applySmoothCommand.argtypes=[ndpointer(dtype=ctypes.c_double),
                                                ctypes.c_char,
                                                ndpointer(dtype=ctypes.c_int)]

    def DM_open(self):

        if DMirror.dll_loaded == True:
            return dm.mro_open(ctypes.byref(self.status))

    def DM_close(self):
        if DMirror.dll_loaded == True:
            return dm.mro_close(ctypes.byref(self.status))

    def DM_applySmoothCommand(self,command,trig):
        if DMirror.dll_loaded == True:
            return dm.mro_applySmoothCommand(command,trig,ctypes.byref(self.status))