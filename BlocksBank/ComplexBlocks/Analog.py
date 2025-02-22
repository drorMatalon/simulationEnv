import numpy as np
from ..CommonFun import *
from BlocksBank.BaseBlocks import *
from BlocksBank.ComplexBlocks import *
from BlocksBank.OtherBlocks import *

class Analog:

    def __init__(self, simCore, index):
    
        self.mSimCore = simCore
        self.mIndex = str(index)
        self.mType = "Analog"
        self.mName = "Analog" + self.mIndex
        self.mSimCore.RegisterBlock(self)
        self.mBlocksDict = {}
        self.mRegsDict = {}
        self.BuildBlocks()
        self.BuildRegisters()
        self.mInput = None
        self.mOutput = None
        
    def BuildBlocks(self):
    
        self.mBlocksDict["Analog" + self.mIndex + "Awgn"] = BbAwgn("Analog" + self.mIndex + "Awgn", self.mSimCore)
        self.mBlocksDict["Analog" + self.mIndex + "Sdr"] = BbPlutoSdr("Analog" + self.mIndex + "Sdr", self.mSimCore)
        self.mSimCore.Connect("Analog" + self.mIndex + "Awgn",
                              "Analog" + self.mIndex + "Sdr")    

    def BuildRegisters(self):
        
        self.mRegsDict["Analog" + self.mIndex + "AwgnReg"] = BbAwgnReg(False, 0.1)
        self.mRegsDict["Analog" + self.mIndex + "SdrReg"] = BbPlutoSdrReg(False, 600000, 1500000000, 1500000000, "slow_attack", -50)
        
        self.mSimCore.InstallReg("Analog" + self.mIndex + "Awgn", self.mRegsDict["Analog" + self.mIndex + "AwgnReg"])
        self.mSimCore.InstallReg("Analog" + self.mIndex + "Sdr", self.mRegsDict["Analog" + self.mIndex + "SdrReg"])

    def GetReg(self, regName):
        if regName in self.mRegsDict:
            return self.mRegsDict[regName]
        else:
            ExitError("Analog num " + self.mIndex + " - No register named " + str(regName) + " -> choose an existing register name")
        
    def ConnectNext(self, block):
        self.mBlocksDict["Analog" + self.mIndex + "Sdr"].ConnectNext(block)

    def CallProccess(self):
        self.mBlocksDict["Analog" + self.mIndex + "Awgn"].mInput = self.mInput
        self.mBlocksDict["Analog" + self.mIndex + "Awgn"].CallProccess()
        self.mOutput = self.mBlocksDict["Analog" + self.mIndex + "Sdr"].mOutput  
        
    def Help(self):
        print("Analog block Proccess:")
        print(" -> Awgn -> Sdr")    
        print("Analog interface:")
        print(" -> GetReg(regName) - returns the relevant register obj")
        print("Analog blocks:")
        for block in self.mBlocksDict:
            print(" -> " + block)
        print("Analog registers:")
        for register in self.mRegsDict:
            print(" -> " + register)