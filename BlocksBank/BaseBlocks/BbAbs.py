import numpy as np
from ..CommonFun import *
from .BaseBlock import BaseBlock

class BbAbs(BaseBlock):

    def __init__(self, name, simCore):
        super().__init__(name, simCore)
        self.mType = "BbAbs"

    def Proccess(self):
        if not self.mSquered:
            self.mOutput = np.abs(self.mInput)
        else:
           self.mOutput = np.abs(self.mInput) ** 2
           
    def LoadConfig(self, register):
        self.mSquered = register.mSquered
        
    def Help(self):
        print("BbAbs block Proccess:")
        print(" -> Returns the absolute value of the input sample")  
        print("BbAbs register(bypass, squered = True):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> squered: if true, returns I^2 + Q^2. else SQRT(I^2 + Q^2)")     
        
class BbAbsReg():

    def __init__(self, bypass, squered = True):
        self.mType = "BbAbsReg"
        self.mByPass = bypass
        self.mSquered = squered
        
    def Update(self, bypass, squered = True):
        self.mByPass = bypass
        self.mSquered = squered