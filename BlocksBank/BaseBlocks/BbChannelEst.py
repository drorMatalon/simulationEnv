import numpy as np
from ..CommonFun import *
from .BaseBlock import BaseBlock

class BbChannelEst(BaseBlock):

    def __init__(self, name, simCore):
        super().__init__(name, simCore)
        self.mType = "BbChannelEst"
        self.mSequence = None

    def Proccess(self):
        matchedFilterOutput = np.convolve(self.mInput, np.conj(self.mSequence[::-1])) 
        filterMax = np.argmax(np.abs(matchedFilterOutput))
        estDelay = filterMax + 1 - len(self.mSequence)
        estScalar = matchedFilterOutput[filterMax] / np.sum(np.abs(self.mSequence) ** 2)
        inverseChannel = np.roll(self.mInput, -estDelay) / estScalar
        self.mOutput = inverseChannel[len(self.mSequence):]
        if self.mSimCore.DBG(4):
            print(self.mName + " - Estimated channel impulse respone = (" + str(estScalar) + ")*delta(n - " + str(estDelay) + ")")
           
    def LoadConfig(self, register):
        if len(register.mSequence) < 1:
            ExitError(self.mName + " - Preamble length must be at least 1 -> add a sequence")
        if len(register.mSequence) % 2 == 1:
            WarningError(self.mName + " - Preamble length is odd -> for more accurate result choose even preamble")
        self.mSequence = np.array(register.mSequence)
        
    def Help(self):
        print("BbChannelEst block Proccess:")
        print(" -> Estimating the channel effect and reverce it (for simple NB channel with weak echo)")
        print(" -> Applies matched filter to find the input sequence location, then views the result peak and estimating the channel phase and gain effect")        
        print("BbChannelEst register(bypass, sequence):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> sequence: sequence values")     
        
class BbChannelEstReg():

    def __init__(self, bypass, sequence):
        self.mType = "BbChannelEstReg"
        self.mByPass = bypass
        self.mSequence = sequence
        
    def Update(self, bypass, sequence):
        self.mByPass = bypass
        self.mSequence = sequence