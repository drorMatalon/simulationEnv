import numpy as np
from ..CommonFun import *

class SimCore:

    def __init__(self):
        self.mType = "SimCore"
        self.mBlocksMap = {}    # [block name] = *block
        self.mInstalledRegisterMap = {}    # [block name] = *register
        self.mMem = {}
        self.mDBGLvl = 0
        self.mDBGExactLvl = True
  
    # ===============
    # Blocks handling
    # ===============
  
    def RegisterBlock(self, block):
        if block.mName in self.mBlocksMap:
            ExitError("Sim core - Double decleration of " + str(block.mName) + " -> change instant name")
        self.mBlocksMap[block.mName] = block
        
    def GetBlock(self, name):
        if name in self.mBlocksMap:
            return self.mBlocksMap[name]
        else:
            ExitError("Sim core - No block named " + str(name) + " -> choose an existing block name")

    def Connect(self, *BlockNameVec):
        if len(BlockNameVec) < 2:
            ExitError("Sim core - Connect function called with less then 2 blocks -> enter more arrguments")
        for i in range(len(BlockNameVec) - 1):      
            PrevBlock = self.GetBlock(BlockNameVec[i])
            PrevBlock.ConnectNext(self.GetBlock(BlockNameVec[i + 1]))

    # =================
    # Register handling
    # =================

    def InstallReg(self, blockName, register, immediately = False):
        if immediately:
            block = self.GetBlock(blockName)
            block.Config(register)
            if self.DBG(1):
                print("Sim core - register installed in " + block.mName, flush = True)
        else:
            self.mInstalledRegisterMap[blockName] = register

    # ===============
    # Memory handling
    # ===============

    def WriteData(self, name, data):
        if name in self.mMem:
            ExitError("Sim core - " + name + " is already registered in memory -> choose a diferent data name")
        if self.DBG(2):
            print("Sim core - WriteData: " + name, flush = True)
        self.mMem[name] = data    

    def ReadData(self, name):
        if name not in self.mMem:
            ExitError("Sim core - " + name + " is not registered in memory -> write data in memory first")
        if self.DBG(2):
            print("Sim core - ReadData: " + name, flush = True)
        return self.mMem[name] 

    # ===================
    # Simulation handling
    # ===================

    def StartFrame(self):
        for key in self.mInstalledRegisterMap:
            block = self.GetBlock(key)
            block.Config(self.mInstalledRegisterMap[key])
            if self.DBG(1):
                print("Sim core - register installed in " + block.mName, flush = True)
        if self.DBG(1):
            print("~~~~~~~~~~~~~~~~~~~~~~~~", flush = True)
            print("Sim core - Frame started", flush = True)
            print("~~~~~~~~~~~~~~~~~~~~~~~~", flush = True)
    
    def DBG(self, DBG_lvl, mode = "R", exact_lvl = True):
        if mode == "R":
            if self.mDBGExactLvl:
                if self.mDBGLvl == DBG_lvl:
                    return True
            else:
                if self.mDBGLvl >= DBG_lvl:
                    return True  
            return False
        if mode == "W":
            self.mDBGLvl = DBG_lvl
            self.mDBGExactLvl = exact_lvl
            return False
        ExitError("Sim core - DBG function mode is not valid -> choose W or R")
        #DBG_lvl 1 - prints proccess
        #DBG_lvl 2 - prints memory access
        #DBG_lvl 3 - prints filters respons
        #DBG_lvl 4 - prints extra information
        
    def Help(self):
        print("SimCore block interface:")
        print("-> StartFrame() - load configurations and starts communication frame")
        print("-> Connect(*BlockName) - connects entered blocks from left (first) to right (last)")
        print("-> InstallReg(blockName, register, immediately = 0) - Install register in the chosen block . if immediately is on loads the configuration immediately")
        print("-> DBG(DBG_lvl, mode = \"R\", exact_lvl = True): mode = \"W\" or \"R\", if exact_lvl = False -  returns true if DBG level <= set level")
        print("-> DBG levels: 0 - None, 1 - System proccess, 2 - Memory access, 3 - Filters respons, 4 - Extra inforamtion")
        print("-> GetBlock(name) - Returns block from the simulation core data base")        
        print("-> WriteData(name, data) - write data with the attached name in the memory")
        print("-> ReadData(name) - read data with the attached name from the memory")