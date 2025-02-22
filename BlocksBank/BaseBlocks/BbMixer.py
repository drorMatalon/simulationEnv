import numpy as np
from ..CommonFun import *
from .BaseBlock import BaseBlock

class BbMixer(BaseBlock):

    def __init__(self, name, simCore):
        super().__init__(name, simCore)
        self.mType = "BbMixer"
        self.mLoFreq = None
        self.mFs = None
        self.mPhase = None
        self.mComplexMode = None

    def Proccess(self):
        arrgument = self.mLoFreq * 2 * np.pi * np.linspace(0, len(self.mInput)-1, len(self.mInput)) / self.mFs + self.mPhase
        if self.mComplexMode:
            loIval = np.cos(arrgument)    
            loQval = np.cos(arrgument+ np.pi / 2)
            self.mOutput = self.mInput.real * loIval + self.mInput.imag * loQval
        else:
            loVal = np.cos(arrgument)
            self.mOutput = loVal * self.mInput
           
    def LoadConfig(self, register):
        self.mLoFreq = register.mLoFreq
        self.mFs = register.mFs
        self.mPhase = register.mPhase
        self.mComplexMode = register.mComplexMode
        if self.mLoFreq >= 1/2 * self.mFs:
            WarnningError(self.mName + " - Lo freq is above nyquist freq -> Better lower the LO freq or increase fs")
        
    def Help(self):
        print("BbMixer block Proccess:")
        print(" -> Simple mixer")  
        print("BbMixer register(bypass, loFreq, fs, phase = 0, complexMode = False):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> loFreq: LO frequency")   
        print(" -> fs = sample rate")
        print(" -> phase: cos wave phase")   
        print(" -> complexMode: If true, multiply the real part by cos(wt+phi) and imagionery by cos(wt + phi + pi/2)")           
        
class BbMixerReg():

    def __init__(self, bypass, loFreq, fs, phase = 0, complexMode = False):
        self.mType = "BbMixerReg"
        self.mByPass = bypass
        self.mLoFreq = loFreq
        self.mFs = fs
        self.mPhase = phase
        self.mComplexMode = complexMode
        
    def Update(self, bypass, loFreq, fs, phase = 0, complexMode = False):
        self.mByPass = bypass
        self.mLoFreq = loFreq
        self.mFs = fs
        self.mPhase = phase
        self.mComplexMode = complexMode