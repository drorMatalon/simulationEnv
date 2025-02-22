import numpy as np
import scipy.signal as signal
from ..CommonFun import *
from .BaseBlock import BaseBlock

class BbIir(BaseBlock):

    def __init__(self, name, simCore):
        super().__init__(name, simCore)
        self.mType = "BbIir"
        self.mNumerator = None
        self.mDenominator = None

    def Proccess(self):
        self.mOutput = signal.lfilter(self.mNumerator, self.mDenominator, self.mInput)
           
    def LoadConfig(self, register):
        self.mNumerator = register.mNumerator
        self.mDenominator = register.mDenominator
        if len(self.mNumerator) < 1 or len(self.mDenominator) < 1:
            ExirError(self.mName + " - numerator or denominator with 0 coefficients -> enter bigger coeeficients list")
        if self.mSimCore.DBG(3) and not self.mByPass:
            PlotFilterRespons(self.mNumerator, self.mDenominator, name = self.mName)

        
    def Help(self):
        print("BbIir block Proccess:")
        print(" -> Simple IIR filter - implement H = (b0 + b1 z^-1 + b2 z^-2 ...)/ (a0 + a1 z^-1 + a2 z^-2 ...)")  
        print("BbIir register(bypass, numerator, denominator):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> numerator: numerator coefficients - [b0, b1, b2 ..]") 
        print(" -> denominator: denominator coefficients - [a0, a1, a2 ..]")        
        
class BbIirReg():

    def __init__(self, bypass, numerator, denominator):
        self.mType = "BbIirReg"
        self.mByPass = bypass
        self.mNumerator = numerator
        self.mDenominator = denominator
        
    def Update(self, bypass, numerator, denominator):
        self.mByPass = bypass
        self.mNumerator = numerator
        self.mDenominator = denominator