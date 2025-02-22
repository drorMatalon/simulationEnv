import numpy as np
from ..CommonFun import *
from .BaseBlock import BaseBlock

class BbGain(BaseBlock):

    def __init__(self, name, simCore):
        super().__init__(name, simCore)
        self.mType = "BbGain"
        self.mIGain = None
        self.mQGain = None

    def Proccess(self):
        self.mOutput = self.mInput.real * self.mIGain + 1j * self.mQGain * self.mInput.imag
           
    def LoadConfig(self, register):
        self.mIGain = register.mIGain
        if register.mQGain is None:
            self.mQGain = register.mIGain
        else:
            self.mQGain = register.mQGain
        
    def Help(self):
        print("BbGain block Proccess:")
        print(" -> Simple linear amplifier")  
        print("BbGain register(bypass, IGain, QGain = IGain):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> IGain: real part gain")
        print(" -> QGain: imaginary part gain")        
        
class BbGainReg():

    def __init__(self, bypass, IGain, QGain = None):
        self.mType = "BbGainReg"
        self.mByPass = bypass
        self.mIGain = IGain
        self.mQGain = QGain
        
    def Update(self, bypass, IGain, QGain = None):
        self.mByPass = bypass
        self.mIGain = IGain
        self.mQGain = QGain