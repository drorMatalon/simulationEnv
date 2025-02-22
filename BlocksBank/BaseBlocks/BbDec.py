import numpy as np
from ..CommonFun import *
from .BaseBlock import BaseBlock

class BbDec(BaseBlock):

    def __init__(self, name, simCore):
        super().__init__(name, simCore)
        self.mType = "BbDec"
        self.mDecFactor = None

    def Proccess(self):
        self.mOutput = self.mInput[::self.mDecFactor]
        
    def LoadConfig(self, register):
        self.mDecFactor = register.mDecFactor
        if self.mDecFactor < 2:
            ExitError(self.mName + " - int factor is less than 2 -> change configuration")
        
    def Help(self):
        print("BbDec block Proccess:")
        print(" -> simple decimator")  
        print("BbDec register(bypass, decFctor):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> decFactor = Decimation rate")      
        
class BbDecReg():

    def __init__(self, bypass, decFactor):
        self.mType = "BbDecReg"
        self.mByPass = bypass
        self.mDecFactor = decFactor
        
    def Update(self, bypass, decFactor):
        self.mByPass = bypass
        self.mDecFactor = decFactor