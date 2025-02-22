from abc import ABC, abstractmethod
from ..CommonFun import *

class BaseBlock(ABC):
    
    def __init__(self, name, simCore):
        self.mName = name
        self.mSimCore = simCore
        self.mSimCore.RegisterBlock(self)
        self.mType = "BaseBlock"
        self.mInput = None
        self.mOutput = None
        self.mNextBlock = None
        self.mByPass = True
        self.mConfigDone = False


    # ==============
    # common methods
    # ==============

    def CallProccess(self):
        self.ValidatePhase()       
        if self.mByPass:
            self.mOutput = self.mInput
        else:
            if self.mSimCore.DBG(1):
                print(self.mName + " - Proccess called", flush = True)
            self.Proccess()
            if self.mSimCore.DBG(1):
                print(self.mName + " - proccess finished", flush = True)       
        if self.mNextBlock is not None:
            self.mNextBlock.mInput = self.mOutput
            self.mNextBlock.CallProccess()

    def Config(self, register):
        if register.mType != self.mType + "Reg":
            ExitError(self.mName + " - register type does not fit blocks type -> change register")
        self.mByPass = register.mByPass
        self.mConfigDone = True
        if self.mByPass:
            return
        self.LoadConfig(register)

    def ConnectNext(self, nextBlock):
        self.mNextBlock = nextBlock 
        if self.mNextBlock.mType == "InGate" or self.mNextBlock.mType == "Tx":
            ExitError(self.mName + " - Connected next block is InGate -> Remove connection") 

    def ValidatePhase(self):
        if self.mInput is None:
            ExitError(self.mName + " - No input -> add input or DBG previous block")
        if self.mConfigDone == False:
            ExitError(self.mName + " - No defined configuration -> Config first")  

    # =======================
    # unique abstract methods
    # =======================
    
    @abstractmethod
    def Proccess(self):
        pass
        # Fill with block functionallity

    @abstractmethod
    def LoadConfig(self, register):
        pass
        #load configuration from register
        
    @abstractmethod
    def Help(self):
        print("BaseBlock block interface:")
        print("Constructor(name, simCore):")
        print("-> name - block name to print in log")
        print("-> simCore - simulation core")
        print("Methods:")
        print("-> ConnectNext(block) - connects the next BbBlock")
        print("-> CallProccess() - initielize the block preccess. Calls the next block preccess when finishes")
        print("     - Add an explenation of the blocks proccess")
        print("-> LoadConfig(register) - load configuration:")
        print("     - Add explention of the register structure")
        #prints the blocks interface