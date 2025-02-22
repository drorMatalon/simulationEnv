import numpy as np
from ..CommonFun import *
from BlocksBank.BaseBlocks import *
from BlocksBank.ComplexBlocks import *
from BlocksBank.OtherBlocks import *

class Tx:

    def __init__(self, simCore, index):
    
        self.mSimCore = simCore
        self.mIndex = str(index)
        self.mType = "Tx"
        self.mName = "Tx" + self.mIndex
        self.mSimCore.RegisterBlock(self)
        self.mBlocksDict = {}
        self.mRegsDict = {}
        self.BuildBlocks()
        self.BuildRegisters()
        self.mInput = None
        self.mOutput = None
        
    def BuildBlocks(self):
    
        self.mBlocksDict["Tx" + self.mIndex + "InGate"] = InGate("Tx" + self.mIndex + "InGate", self.mSimCore)
        self.mBlocksDict["Tx" + self.mIndex + "Int"] = BbInt("Tx" + self.mIndex + "Int", self.mSimCore)
        self.mBlocksDict["Tx" + self.mIndex + "Fir_0"] = BbFir("Tx" + self.mIndex + "Fir_0", self.mSimCore)
        self.mBlocksDict["Tx" + self.mIndex + "Gain"] = BbGain("Tx" + self.mIndex + "Gain", self.mSimCore)
        self.mBlocksDict["Tx" + self.mIndex + "Mixer"] = BbMixer("Tx" + self.mIndex + "Mixer", self.mSimCore)
        self.mBlocksDict["Tx" + self.mIndex + "Preamble"] = BbPreamble("Tx" + self.mIndex + "Preamble", self.mSimCore)
        self.mBlocksDict["Tx" + self.mIndex + "Fir_1"] = BbFir("Tx" + self.mIndex + "Fir_1", self.mSimCore)
        self.mSimCore.Connect("Tx" + self.mIndex + "InGate",
                              "Tx" + self.mIndex + "Int",
                              "Tx" + self.mIndex + "Fir_0",
                              "Tx" + self.mIndex + "Gain",
                              "Tx" + self.mIndex + "Mixer",
                              "Tx" + self.mIndex + "Preamble",
                              "Tx" + self.mIndex + "Fir_1")    

    def BuildRegisters(self):
        
        self.mRegsDict["Tx" + self.mIndex + "IntReg"] = BbIntReg(True, 20)
        self.mRegsDict["Tx" + self.mIndex + "Fir0Reg"] = BbFirReg(True, np.ones(20))
        self.mRegsDict["Tx" + self.mIndex + "GainReg"] = BbGainReg(True, 1/20)
        self.mRegsDict["Tx" + self.mIndex + "MixerReg"] = BbMixerReg(True, 100, 500)
        self.mRegsDict["Tx" + self.mIndex + "PreambleReg"] = BbPreambleReg(True, [2, 1, 0, -1, -2, -1, 0, 1, 2, 1, 0, -1, -2, -1])
        self.mRegsDict["Tx" + self.mIndex + "Fir1Reg"] = BbFirReg(True, signal.firwin(16, 150, fs=500, window="hamming"))
        
        self.mSimCore.InstallReg("Tx" + self.mIndex + "Int", self.mRegsDict["Tx" + self.mIndex + "IntReg"])
        self.mSimCore.InstallReg("Tx" + self.mIndex + "Fir_0", self.mRegsDict["Tx" + self.mIndex + "Fir0Reg"])
        self.mSimCore.InstallReg("Tx" + self.mIndex + "Gain", self.mRegsDict["Tx" + self.mIndex + "GainReg"])
        self.mSimCore.InstallReg("Tx" + self.mIndex + "Mixer", self.mRegsDict["Tx" + self.mIndex + "MixerReg"])
        self.mSimCore.InstallReg("Tx" + self.mIndex + "Preamble", self.mRegsDict["Tx" + self.mIndex + "PreambleReg"])
        self.mSimCore.InstallReg("Tx" + self.mIndex + "Fir_1", self.mRegsDict["Tx" + self.mIndex + "Fir1Reg"])

    def GetReg(self, regName):
        if regName in self.mRegsDict:
            return self.mRegsDict[regName]
        else:
            ExitError("Tx num " + self.mIndex + " - No register named " + str(regName) + " -> choose an existing register name")
        
    def ConnectNext(self, block):
        self.mBlocksDict["Tx" + self.mIndex + "Mixer"].ConnectNext(block)
        
    def Help(self):
        print("Tx block Proccess:")
        print(" -> TxInGate -> Fir_0 (Pulse shaping) -> Gain -> Mixer -> Preamble -> Fir_1 (LPF)") 
        print(" -> remember to connect Tx" + self.mIndex + "Fir_1 to the next block (Analog/ Rx chain)")    
        print("Tx interface:")
        print(" -> GetReg(regName) - returns the relevant register obj")
        print("Tx blocks:")
        for block in self.mBlocksDict:
            print(" -> " + block)
        print("Tx registers:")
        for register in self.mRegsDict:
            print(" -> " + register)