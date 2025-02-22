import numpy as np
from ..CommonFun import *
from BlocksBank.BaseBlocks import *

class BbIQModulator(BaseBlock):

    def __init__(self, name, simCore):
        super().__init__(name, simCore)
        self.mType = "BbIQModulator"
        self.mLpf = BbFir(self.mName + "Lpf", self.mSimCore)
        self.mMixer = BbMixer(self.mName + "Mixer", self.mSimCore)
        self.mLpf.ConnectNext(self.mMixer)
        self.mDcGain = None

    def Proccess(self):
        dcConst = np.ones(len(self.mInput)) * self.mDcGain
        self.mLpf.mInput = self.mInput + dcConst + 1j * dcConst
        if np.min(self.mInput.real) + self.mDcGain < 0 or np.min(self.mInput.imag) + self.mDcGain < 0:
            WarningError(self.mName + " - DC gain value is smaller than the minimal input -> might not work properly")
        self.mLpf.CallProccess()
        self.mOutput = self.mMixer.mOutput
           
    def LoadConfig(self, register):
        self.mDcGain = register.mDcGain 
        self.mSimCore.InstallReg(self.mName + "Lpf", register.mLpfReg, True)
        self.mSimCore.InstallReg(self.mName + "Mixer", register.mMixerReg, True)
        
    def Help(self):
        print("BbIQModulator block Proccess:")
        print(" -> IQ modulator - a + jb -> a cos(wt) - b sin(wt)")  
        print("BbIQModulator register(bypass, dcGain, loFreq, coefficients):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> dcGain: constant add (complex), to enable edge detection")
        print(" -> loFreq: carrier wave frequency")
        print(" -> coefficients: FIR coeeficients - LPF filter implementation, might changed in the future")        
        
class BbIQModulatorReg():

    def __init__(self, bypass, dcGain, loFreq, fs, coefficients):
        self.mType = "BbIQModulatorReg"
        self.mByPass = bypass
        self.mDcGain = dcGain
        self.mLpfReg = BbFirReg(bypass, coefficients)
        self.mMixerReg = BbMixerReg(bypass, loFreq, fs, 0, True)
        
    def Update(self, bypass, dcGain, loFreq, fs, coefficients):
        self.mByPass = bypass
        self.mDcGain = dcGain
        self.mLpfReg.Update(bypass, coefficients)
        self.mMixerReg.Update(bypass, loFreq, fs, 0, True)