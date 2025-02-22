import numpy as np
from ..CommonFun import *
from .BaseBlock import BaseBlock

class BbDetector(BaseBlock):

    def __init__(self, name, simCore):
        super().__init__(name, simCore)
        self.mType = "BbDetector"
        self.mModulation = None
        self.mValidModulations = ["BPSK", "QPSK", "8PSK", "16PSK", "4QAM", "16QAM", "64QAM"]

    def Proccess(self):
        possibleSymbolesArr = None
        if self.mModulation == "BPSK":
            possibleSymbolesArr = np.array((1, -1))
        elif self.mModulation == "QPSK":
            possibleSymbolesArr = np.exp(1j * np.pi * np.arange(4) / 2 + 1j * np.pi / 4)
        elif self.mModulation == "8PSK":
            possibleSymbolesArr = np.exp(1j * np.pi * np.arange(8) / 4)
        elif self.mModulation == "16PSK":
            possibleSymbolesArr = np.exp(1j * np.pi * np.arange(16) / 8)
        elif self.mModulation == "4QAM":
            possibleSymbolesArr = np.array((1 + 1j, 1 + -1j, -1 + 1j, -1 - 1j))
        elif self.mModulation == "16QAM":
            real = np.array([-3, -1, 1, 3])
            imag = np.array([-3, -1, 1, 3])
            possibleSymbolesArr = np.array([r + 1j * i for r in real for i in imag])           
        elif self.mModulation == "64QAM":
            real = np.array([-7, -5, -3, -1, 1, 3, 5, 7])
            imag = np.array([-7, -5, -3, -1, 1, 3, 5, 7])
            possibleSymbolesArr = np.array([r + 1j * i for r in real for i in imag])           
        else:
            ExitError(self.mName + " - Not implemented yet!")
        self.mOutput = []
        distanceVec = []
        for sample in self.mInput:
            closestSymbole, dist = self.Closest(sample, possibleSymbolesArr)
            self.mOutput.append(closestSymbole)
            distanceVec.append(dist)
        if self.mSimCore.DBG(4):
            avgDist =  np.sqrt(np.average(np.square(distanceVec)))
            avgAmplitude = np.sqrt(np.average(np.square(np.abs(self.mOutput))))
            EVM = avgDist / avgAmplitude
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(self.mName + " - Calculated EVM = " + str(EVM))
            print("Average distance between samples and closest symboles = " + str(avgDist))
            print("Approximate SNR = " + str(1 / EVM / EVM))            
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            
    def Closest(self, sample, possibleSymbolesArr):
        minDist = None
        closestSymbole = None
        for symbole in possibleSymbolesArr:
            dist = np.abs(sample - symbole)
            if minDist is None:
                minDist = dist
                closestSymbole = symbole
            elif dist < minDist:
                minDist = dist
                closestSymbole = symbole   
        return closestSymbole, minDist
           
    def LoadConfig(self, register):
        self.mModulation = register.mModulation
        if self.mModulation not in self.mValidModulations:
            ExitError(self.mName + " - chosen modulation type is not valid -> chose one among: BPSK, QPSK, 8PSK, 16PSK, 4QAM, 16QAM, 64QAM")
        
    def Help(self):
        print("BbDetector block Proccess:")
        print(" -> attached to every sample the closest symbol assuming equal distribution")  
        print("BbDetector register(bypass, modulation):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> modulation: modulation type (supports BPSK, QPSK, 8PSK, 16PSK, 4QAM, 16QAM, 64QAM)")       
        
class BbDetectorReg():

    def __init__(self, bypass, modulation):
        self.mType = "BbDetectorReg"
        self.mByPass = bypass
        self.mModulation = modulation
        
    def Update(self, bypass, modulation):
        self.mByPass = bypass
        self.mModulation = modulation