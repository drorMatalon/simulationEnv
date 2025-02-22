import numpy as np
from ..CommonFun import *
from BlocksBank.BaseBlocks import *

class BbEdgeDetector(BaseBlock):

    def __init__(self, name, simCore):
        super().__init__(name, simCore)
        self.mType = "BbEdgeDetector"
        self.mDiode = BbDiode(self.mName + "Diode", self.mSimCore)
        self.mLpf = BbFir(self.mName + "Lpf", self.mSimCore)
        self.mGain = BbGain(self.mName + "Gain", self.mSimCore)
        self.mDiode.ConnectNext(self.mLpf)
        self.mLpf.ConnectNext(self.mGain)

    def Proccess(self):
        self.mDiode.mInput = self.mInput
        self.mDiode.CallProccess()
        self.mOutput = self.mGain.mOutput
           
    def LoadConfig(self, register):
        self.mSimCore.InstallReg(self.mName + "Diode", register.mDiodeReg, True)
        self.mSimCore.InstallReg(self.mName + "Lpf", register.mLpfReg, True)
        self.mSimCore.InstallReg(self.mName + "Gain", register.mGainReg, True)
        
    def Help(self):
        print("BbEdgeDetector block Proccess:")
        print(" -> Extract the envalope of a signal: diode -> LPF -> gain")  
        print("BbEdgeDetector register(bypass, coefficients):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> coefficients: FIR coefficient, act as LPF")       
        
class BbEdgeDetectorReg():

    def __init__(self, bypass, coefficients):
        self.mType = "BbEdgeDetectorReg"
        self.mByPass = bypass
        self.mDiodeReg = BbDiodeReg(bypass, "full bridge")
        self.mLpfReg = BbFirReg(bypass, coefficients)
        self.mGainReg = BbGainReg(bypass, np.pi / 2)
        
    def Update(self, bypass, coefficients):
        self.mByPass = bypass
        self.mDiodeReg.Update(bypass, "full bridge")
        self.mLpfReg.Update(bypass, coefficients)
        self.mGainReg.Update(bypass, np.pi / 2)