import numpy as np
from ..CommonFun import *
from .BaseBlock import BaseBlock

class BbPreamble(BaseBlock):

    def __init__(self, name, simCore):
        super().__init__(name, simCore)
        self.mType = "BbPreamble"
        self.mSequence = None

    def Proccess(self):
        self.mOutput = np.concatenate((self.mSequence, self.mInput))        
           
    def LoadConfig(self, register):
        if len(register.mSequence) < 1:
            ExitError(self.mName + " - Preamble length must be at least 1 -> add a sequence")
        self.mSequence = np.array(register.mSequence)
        
    def Help(self):
        print("BbPreamble block Proccess:")
        print(" -> Add a known sequence to the beggining of the trassmition")  
        print("BbPreamble register(bypass, sequence):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> sequence: sequence values")     
        
class BbPreambleReg():

    def __init__(self, bypass, sequence):
        self.mType = "BbPreambleReg"
        self.mByPass = bypass
        self.mSequence = sequence
        
    def Update(self, bypass, sequence):
        self.mByPass = bypass
        self.mSequence = sequence