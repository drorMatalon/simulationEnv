import numpy as np
from ..CommonFun import *
from .BaseBlock import BaseBlock

class BbInt(BaseBlock):

    def __init__(self, name, simCore):
        super().__init__(name, simCore)
        self.mType = "BbInt"
        self.mIntFactor = None

    def Proccess(self):
        self.mOutput = np.zeros(len(self.mInput) * self.mIntFactor, dtype=self.mInput.dtype)
        self.mOutput[::self.mIntFactor] = self.mInput
        
    def LoadConfig(self, register):
        self.mIntFactor = register.mIntFactor
        if self.mIntFactor < 2:
            ExitError(self.mName + " - int factor is less than 2 -> change configuration")
        
    def Help(self):
        print("BbInt block Proccess:")
        print(" -> Delta interpulator")  
        print("BbInt register(bypass, intFactor):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> intFactor = interpulation rate")      
        
class BbIntReg():

    def __init__(self, bypass, intFactor):
        self.mType = "BbIntReg"
        self.mByPass = bypass
        self.mIntFactor = intFactor
        
    def Update(self, bypass, intFactor):
        self.mByPass = bypass
        self.mIntFactor = intFactor