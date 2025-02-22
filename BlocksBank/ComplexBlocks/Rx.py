import numpy as np
from ..CommonFun import *
from BlocksBank.BaseBlocks import *
from BlocksBank.ComplexBlocks import *
from BlocksBank.OtherBlocks import *

class Rx:

    def __init__(self, simCore, index):
    
        self.mSimCore = simCore
        self.mIndex = str(index)
        self.mType = "Rx"
        self.mName = "Rx" + self.mIndex
        self.mSimCore.RegisterBlock(self)
        self.mBlocksDict = {}
        self.mRegsDict = {}
        self.BuildBlocks()
        self.BuildRegisters()
        self.mInput = None
        self.mOutput = None
        
    def BuildBlocks(self):
    
        self.mBlocksDict["Rx" + self.mIndex + "Iir_0"] = BbIir("Rx" + self.mIndex + "Iir_0", self.mSimCore)
        self.mBlocksDict["Rx" + self.mIndex + "Iir_1"] = BbIir("Rx" + self.mIndex + "Iir_1", self.mSimCore)
        self.mBlocksDict["Rx" + self.mIndex + "ChannelEst"] = BbChannelEst("Rx" + self.mIndex + "ChannelEst", self.mSimCore)
        self.mBlocksDict["Rx" + self.mIndex + "Abs"] = BbAbs("Rx" + self.mIndex + "Abs", self.mSimCore)
        self.mBlocksDict["Rx" + self.mIndex + "Fir_0"] = BbFir("Rx" + self.mIndex + "Fir_0", self.mSimCore)
        self.mBlocksDict["Rx" + self.mIndex + "Fir_1"] = BbFir("Rx" + self.mIndex + "Fir_1", self.mSimCore)
        self.mBlocksDict["Rx" + self.mIndex + "Gain"] = BbGain("Rx" + self.mIndex + "Gain", self.mSimCore)
        self.mBlocksDict["Rx" + self.mIndex + "Dec"] = BbDec("Rx" + self.mIndex + "Dec", self.mSimCore)
        self.mBlocksDict["Rx" + self.mIndex + "Detector"] = BbDetector("Rx" + self.mIndex + "Detector", self.mSimCore)
        self.mSimCore.Connect("Rx" + self.mIndex + "Iir_0",
                              "Rx" + self.mIndex + "Iir_1",
                              "Rx" + self.mIndex + "ChannelEst",
                              "Rx" + self.mIndex + "Abs",
                              "Rx" + self.mIndex + "Fir_0",
                              "Rx" + self.mIndex + "Fir_1",
                              "Rx" + self.mIndex + "Gain",
                              "Rx" + self.mIndex + "Dec",
                              "Rx" + self.mIndex + "Detector")    

    def BuildRegisters(self):
        
        self.mRegsDict["Rx" + self.mIndex + "Iir0Reg"] = BbIirReg(True, [1, -2 * np.cos(np.pi/2), 1], [1, -2 * 0.95 * np.cos(np.pi/2), 0.95 * 0.95])
        self.mRegsDict["Rx" + self.mIndex + "Iir1Reg"] = BbIirReg(True, [1, -1], [1, -0.99])
        self.mRegsDict["Rx" + self.mIndex + "ChannelEstReg"] = BbChannelEstReg(True, [2, 1, 0, -1, -2, -1, 0, 1, 2, 1, 0, -1, -2, -1])      
        self.mRegsDict["Rx" + self.mIndex + "AbsReg"] = BbAbsReg(True, False)
        self.mRegsDict["Rx" + self.mIndex + "Fir0Reg"] = BbFirReg(True, signal.firwin(16, 150, fs=500, window="hamming"))
        self.mRegsDict["Rx" + self.mIndex + "Fir1Reg"] = BbFirReg(True, np.ones(20))
        self.mRegsDict["Rx" + self.mIndex + "GainReg"] = BbGainReg(True, 1/20)
        self.mRegsDict["Rx" + self.mIndex + "DecReg"] = BbDecReg(True, 20)
        self.mRegsDict["Rx" + self.mIndex + "DetectorReg"] = BbDetectorReg(True, "BPSK")
        
        self.mSimCore.InstallReg("Rx" + self.mIndex + "Iir_0", self.mRegsDict["Rx" + self.mIndex + "Iir0Reg"])
        self.mSimCore.InstallReg("Rx" + self.mIndex + "Iir_1", self.mRegsDict["Rx" + self.mIndex + "Iir1Reg"])
        self.mSimCore.InstallReg("Rx" + self.mIndex + "ChannelEst", self.mRegsDict["Rx" + self.mIndex + "ChannelEstReg"])
        self.mSimCore.InstallReg("Rx" + self.mIndex + "Abs", self.mRegsDict["Rx" + self.mIndex + "AbsReg"])
        self.mSimCore.InstallReg("Rx" + self.mIndex + "Fir_0", self.mRegsDict["Rx" + self.mIndex + "Fir0Reg"])
        self.mSimCore.InstallReg("Rx" + self.mIndex + "Fir_1", self.mRegsDict["Rx" + self.mIndex + "Fir1Reg"])
        self.mSimCore.InstallReg("Rx" + self.mIndex + "Gain", self.mRegsDict["Rx" + self.mIndex + "GainReg"])
        self.mSimCore.InstallReg("Rx" + self.mIndex + "Dec", self.mRegsDict["Rx" + self.mIndex + "DecReg"])
        self.mSimCore.InstallReg("Rx" + self.mIndex + "Detector", self.mRegsDict["Rx" + self.mIndex + "DetectorReg"])

    def GetReg(self, regName):
        if regName in self.mRegsDict:
            return self.mRegsDict[regName]
        else:
            ExitError("RX num " + self.mIndex + " - No register named " + str(regName) + " -> choose an existing register name")
            
    def CallProccess(self):
        self.mBlocksDict["Rx" + self.mIndex + "Iir_0"].mInput = self.mInput
        self.mBlocksDict["Rx" + self.mIndex + "Iir_0"].CallProccess()
        self.mOutput = self.mBlocksDict["Rx" + self.mIndex + "Detector"].mOutput        
 
    def ConnectNext(self, block):
        self.mBlocksDict["Rx" + self.mIndex + "Detector"].ConnectNext(block)
 
    def Help(self):
        print("RX block Proccess:")
        print(" -> IIR0 -> IIR1 (Notched groupe) -> channel est -> Abs -> FIR_0 (LPF/ BPF) -> FIR_1 (Matched filter) -> Gain -> Decimator -> Detector") 
        print(" -> remember to connect Rx" + self.mIndex + "Iir_0 to the previus block (Analog/ Tx chain)")    
        print("RX interface:")
        print(" -> GetReg(regName) - returns the relevant register obj")
        print("Rx blocks:")
        for block in self.mBlocksDict:
            print(" -> " + block)
        print("Rx registers:")
        for register in self.mRegsDict:
            print(" -> " + register)