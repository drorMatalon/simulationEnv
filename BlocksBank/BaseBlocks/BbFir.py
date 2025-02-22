import numpy as np
from ..CommonFun import *
from .BaseBlock import BaseBlock

class BbFir(BaseBlock):

    def __init__(self, name, simCore):
        super().__init__(name, simCore)
        self.mType = "BbFir"
        self.mCoeff = None

    def Proccess(self):
        self.mOutput = np.convolve(self.mInput, self.mCoeff, mode='same')
        
           
    def LoadConfig(self, register):
        self.mCoeff = register.mCoeff
        if len(self.mCoeff) < 1:
            ExirError(self.mName + " - 0 coefficients -> enter bigger coeeficients list")
        if self.mSimCore.DBG(3) and not self.mByPass:
            PlotFilterRespons(self.mCoeff, name = self.mName)
        
    def Help(self):
        print("BbFir block Proccess:")
        print(" -> Simple FIR filter")  
        print("BbFir register(bypass, coefficients):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> coefficients: FIR coefficients")     
        
class BbFirReg():

    def __init__(self, bypass, coefficients):
        self.mType = "BbFirReg"
        self.mByPass = bypass
        self.mCoeff = coefficients
        
    def Update(self, bypass, coefficients):
        self.mByPass = bypass
        self.mCoeff = coefficients