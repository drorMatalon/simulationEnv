import numpy as np
import scipy.signal as signal
from BlocksBank.BaseBlocks import *
from BlocksBank.OtherBlocks import *
from BlocksBank.Modulators import *
from BlocksBank.CommonFun import *

simCore = SimCore()
simCore.DBG(3, "W", 0)

Sdr = BbPlutoSdr("Sdr", simCore)
Scope = Analyzer("Scope_0", simCore)

"""
TX chain: in gate -> interpulator -> FIR (for pulse shaping) -> gain -> sdr
"""

TxInGate = InGate("TxInGate_0", simCore)
TxInt = BbInt("TxInterpulator", simCore)
TxFir = BbFir("TxFir", simCore)
TxGain = BbGain("TxGain", simCore)
simCore.Connect("TxInGate_0", "TxInterpulator", "TxFir", "TxGain", "Sdr")

"""
Rx chain: sdr -> IIR -> IIR (Notched) -> FIR (Matched filter) -> Decimator -> gain
"""

RxIir0 = BbIir("RxIir_0", simCore)
RxIir1 = BbIir("RxIir_1", simCore)
RxFir = BbFir("RxFir", simCore)
RxGain = BbGain("RxGain", simCore)
simCore.Connect("Sdr", "RxIir_0", "RxIir_1", "RxFir", "RxGain")

"""
Registers generation and installation
"""

TxIntReg = BbIntReg(True, 1)
TxFirReg = BbFirReg(True, np.ones(10))
TxGainReg = BbGainReg(True, 1)

simCore.InstallReg("TxInterpulator", TxIntReg)
simCore.InstallReg("TxFir", TxFirReg)
simCore.InstallReg("TxGain", TxGainReg)

SdrReg = BbPlutoSdrReg(False, 600000, 1500000000, 1500000000, "slow_attack", -50)
simCore.InstallReg("Sdr", SdrReg)

RxIir0Reg = BbIirReg(True, [1], [1])
RxIir1Reg = BbIirReg(True, [1], [1])
RxFirReg = BbFirReg(True, np.ones(10))
RxGainReg = BbGainReg(True, 1)

simCore.InstallReg("RxIir_0", RxIir0Reg)
simCore.InstallReg("RxIir_1", RxIir1Reg)
simCore.InstallReg("RxFir", RxFirReg)
simCore.InstallReg("RxGain", RxGainReg)

"""
Trassmition
"""

#Simple cos wave trassmition. The I and Q signls are mixed in the analyzer scince they have global phase
t = np.linspace(0, 1023, 1024) / 600000 #Trassmition of 1024 / 600000 seconds ~ 1 / 600 seconds
testSig = np.cos(2 * np.pi * 2100 * t) + 1j * np.cos(2 * np.pi * 4500 * t)

simCore.StartFrame()
TxInGate.GetSamples(testSig)

Scope.Connect("Sdr")  
#Scope.Plot("power")


#Trassmiting two signls
t = np.linspace(0, 1023, 1024) / 600000 
testSig = np.cos(2 * np.pi * 120000 * t) + np.cos(2 * np.pi * 150000 * t)
SdrReg.Update(False, 600000, 2400000000, 2400000000, 50, -0)

simCore.StartFrame()
TxInGate.GetSamples(testSig)

Scope.Connect("Sdr")  
Scope.Plot("fft")

IM3_high = (2 * 150000 - 120000)/ 600000 * 2 * np.pi
IM3_low = (2 * 120000 - 150000)/ 600000 * 2 * np.pi

RxIir0Reg.Update(False, [1, -2 * np.cos(IM3_high), 1], [1, -2 * 0.95 * np.cos(IM3_high), 0.95 * 0.95])
RxIir1Reg.Update(False, [1, -2 * np.cos(IM3_low), 1], [1, -2 * 0.95 * np.cos(IM3_low), 0.95 *0.95])

simCore.StartFrame()
TxInGate.GetSamples(testSig)

Scope.Connect("RxIir_1")  
Scope.Plot("fft")

del Sdr.mSdr