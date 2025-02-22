import numpy as np
import scipy.signal as signal
from BlocksBank.BaseBlocks import *
from BlocksBank.OtherBlocks import *
from BlocksBank.Modulators import *
from BlocksBank.CommonFun import *

simCore = SimCore()
simCore.DBG(1, "W", 1)

IG = InGate("InGate_0", simCore)
IQMod = BbIQModulator("IqMod_0", simCore)
EdgeDetector = BbEdgeDetector("EdgeDetector_0", simCore)

simCore.Connect("InGate_0", "IqMod_0", "EdgeDetector_0")

IqModReg = BbIQModulatorReg(False, 1, 100, 1000, signal.firwin(30, 10, fs=1000, window = "blackman"))
EdgeDetectorReg = BbEdgeDetectorReg(False, signal.firwin(30, 10, fs=1000, window = "blackman"))

simCore.InstallReg("IqMod_0", IqModReg)
simCore.InstallReg("EdgeDetector_0", EdgeDetectorReg)

simCore.StartFrame()
IG.GetSamples(np.cos(np.pi * 2 / 100 * np.linspace(0, 999, 1000)))

Scope = Analyzer("Scope_0", simCore)
Scope.Connect("EdgeDetector_0")  
Scope.Plot("power")

