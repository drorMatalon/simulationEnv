import numpy as np
from ..CommonFun import *

class InGate:

    def __init__(self, name, simCore):
        self.mName = name
        self.mSimCore = simCore
        self.mSimCore.RegisterBlock(self)
        self.mType = "InGate"
        self.mInput = None
        self.mOutput = None
        self.mNextBlock = None

    def GetSamples(self, inputList):
        self.mInput = np.array(inputList)
        if self.mNextBlock is None:
            ExitError(self.mName + " - In gate with no block connected -> connect next block")
        self.mNextBlock.mInput = self.mInput
        self.mNextBlock.CallProccess()

    def GenSig(self, N, modulation):
        inSamples = None
        if N < 1:
            ExitError(self.mName + " - input signal length is less then 1 -> chose valid N arrgument")
        if modulation == "BPSK":
            inSamples = self.PSK(2, N)               
        elif modulation == "QPSK":            
            inSamples = self.PSK(4, N, np.pi / 4) 
        elif modulation == "8PSK":            
            inSamples = self.PSK(8, N, np.pi / 4)
        elif modulation == "16PSK":            
            inSamples = self.PSK(16, N, np.pi / 4)
        elif modulation == "4QAM":            
            inSamples = self.QAM(4, N, 2) 
        elif modulation == "16QAM":            
            inSamples = self.QAM(16, N, 2) 
        elif modulation == "64QAM":            
            inSamples = self.QAM(64, N, 2)             
        else:
            ExitError(self.mName + " - chosen mode is not supported -> choose BPSK, QPSK, 8PSK, 16PSK, 4QAM, 16QAM, 64QAM")
        self.GetSamples(inSamples)
            
    def PSK(self, order, N, phase = 0):
        x = np.random.randint(0, order, N)
        x = np.exp(1j * 2 * np.pi * x / order + 1j * phase)
        x = np.round(x, 2)
        return x

    def QAM(self, order, N, gain = 1):
        M = int(np.sqrt(order))
        I = np.random.randint(0, M, N) - (M-1)/2
        Q = np.random.randint(0, M, N) - (M-1)/2
        return gain * (I + 1j * Q)

    def ConnectNext(self, nextBlock):
        self.mNextBlock = nextBlock 
        
    def Help(self):
        print("InGate perpuse:")
        print("-> Get inputs from the user")
        print("GetSamples(inputList):")
        print("-> Add input samples")
        print("GenSig(N, modulation): create N symbols length signal of the chosen modulation")
        print("-> modulations types: BPSK, QPSK, 8PSK, 4QAM, 16QAM")