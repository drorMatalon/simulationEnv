import numpy as np
from ..CommonFun import *
from .BaseBlock import BaseBlock

class BbAwgn(BaseBlock):

    def __init__(self, name, simCore):
        super().__init__(name, simCore)
        self.mType = "BbAwgn"
        self.mN0 = None

    def Proccess(self):
        N = np.random.normal(0, np.sqrt(self.mN0/2), len(self.mInput)) + 1j * np.random.normal(0, np.sqrt(self.mN0/2), len(self.mInput))
        self.mOutput = self.mInput + N
        
    def LoadConfig(self, register):
        self.mN0 = register.mN0
        
    def Help(self):
        print("BbAwgn block Proccess:")
        print(" -> Add a white gaussian noise with Sn = N0\2")  
        print("BbAwgnReg register(bypass, N0):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> N0: Noise power spectral densety level")      
        
class BbAwgnReg():

    def __init__(self, bypass, N0):
        self.mType = "BbAwgnReg"
        self.mByPass = bypass
        self.mN0 = N0
        
    def Update(self, bypass, N0):
        self.mByPass = bypass
        self.mN0 = N0