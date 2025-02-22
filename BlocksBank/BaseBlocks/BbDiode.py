import numpy as np
from ..CommonFun import *
from .BaseBlock import BaseBlock

class BbDiode(BaseBlock):

    def __init__(self, name, simCore):
        super().__init__(name, simCore)
        self.mType = "BbDiode"
        self.mMode = None

    def Proccess(self):
        realPart = self.mInput.real
        imagPart = self.mInput.imag     
        if self.mMode == "half bridge":
            realPart = np.where(realPart > 0, realPart, 0)
            imagPart = np.where(imagPart > 0, imagPart, 0)
            self.mOutput = realPart + 1j * imagPart
        if self.mMode == "full bridge":
            realPart = np.abs(realPart)
            imagPart = np.abs(imagPart)
            self.mOutput = realPart + 1j * imagPart
           
    def LoadConfig(self, register):
        if register.mMode != "half bridge" and register.mMode != "full bridge":
            ExitError(self.mName + " - chosen operation mode is not valid -> choose half bridge or full bridge")
        self.mMode = register.mMode
        
    def Help(self):
        print("BbDiode block Proccess:")
        print(" -> Passes only positive samples. For complex input, returns works on rel and imagionary part seperately")  
        print("BbDiode register(bypass, gain):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> mode: half bridge, full bridge")     
        
class BbDiodeReg():

    def __init__(self, bypass, mode):
        self.mType = "BbDiodeReg"
        self.mByPass = bypass
        self.mMode = mode
        
    def Update(self, bypass, mode):
        self.mByPass = bypass
        self.mMode = mode