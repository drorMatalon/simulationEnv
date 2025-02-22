import numpy as np
import scipy.signal as signal
from BlocksBank.BaseBlocks import *
from BlocksBank.OtherBlocks import *
from BlocksBank.ComplexBlocks import *
from BlocksBank.CommonFun import *

simCore = SimCore()
simCore.DBG(4, "W", 1)

Scope = Analyzer("Scope_0", simCore)

"""
TX chain: in gate -> interpulator -> FIR (for pulse shaping) -> gain -> mixer -> preamble -> Analog
"""

TxInGate = InGate("TxInGate_0", simCore)
TxInt = BbInt("TxInterpulator", simCore)
TxFir = BbFir("TxFir", simCore)
TxGain = BbGain("TxGain", simCore)
TxMixer = BbMixer("TxMixer", simCore)
TxPreamble = BbPreamble("TxPreamble", simCore)

simCore.Connect("TxInGate_0", "TxInterpulator", "TxFir", "TxGain", "TxMixer", "TxPreamble")

"""
Rx chain: Analog -> IIR0 (Notched) -> IIR1 (Notched) -> channel estimator -> Absolut value -> FIR_0 -> FIR_1 (Matched filter) -> Decimator -> gain
"""

RxIir0 = BbIir("RxIir_0", simCore)
RxIir1 = BbIir("RxIir_1", simCore)
RxChannelEst = BbChannelEst("RxChannelEst", simCore)
RxAbs = BbAbs("RxAbs", simCore)
RxFir = BbFir("RxFir_0", simCore)
RxFir = BbFir("RxFir_1", simCore)
RxDec = BbDec("RxDec", simCore)
RxGain = BbGain("RxGain", simCore)
simCore.Connect("RxIir_0", "RxIir_1", "RxChannelEst", "RxAbs", "RxFir_0", "RxFir_1", "RxGain", "RxDec")

"""
Analog: Awgn or Sdr, disable one of them!
"""

Awgn = BbAwgn("Awgn", simCore)
Sdr = BbPlutoSdr("Sdr", simCore)
simCore.Connect("TxPreamble", "Awgn", "Sdr", "RxIir_0")

"""
Registers generation and installation
"""

TxIntReg = BbIntReg(True, 20)
TxFirReg = BbFirReg(True, np.ones(20))
TxGainReg = BbGainReg(True, 10, 10)
TxMixerReg = BbMixerReg(True, 100, 500)
TxPreambleReg = BbPreambleReg(False, np.array([2, 1, 0, -1, -2, -1, 0, 1, 2, 1, 0, -1, -2, -1]))

simCore.InstallReg("TxInterpulator", TxIntReg)
simCore.InstallReg("TxFir", TxFirReg)
simCore.InstallReg("TxGain", TxGainReg)
simCore.InstallReg("TxMixer", TxMixerReg)
simCore.InstallReg("TxPreamble", TxPreambleReg)

AwgnReg = BbAwgnReg(True, 0.6)
SdrReg = BbPlutoSdrReg(False, 600000, 1500000000, 1500000000, "slow_attack", -50)

simCore.InstallReg("Awgn", AwgnReg)
simCore.InstallReg("Sdr", SdrReg)

RxIir0Reg = BbIirReg(True, [1, -2 * np.cos(np.pi/2), 1], [1, -2 * 0.95 * np.cos(np.pi/2), 0.95 * 0.95])
RxIir1Reg = BbIirReg(True, [1, -2 * np.cos(np.pi/2), 1], [1, -2 * 0.95 * np.cos(np.pi/2), 0.95 *0.95])
RxChannelEstReg = BbChannelEstReg(False, [2, 1, 0, -1, -2, -1, 0, 1, 2, 1, 0, -1, -2, -1])
RxAbsReg = BbAbsReg(True, False)
RxFir0Reg = BbFirReg(True, signal.firwin(16, 150, fs=500, window="hamming"))
RxFir1Reg = BbFirReg(True, np.ones(20))
RxDecReg = BbDecReg(True, 20)
RxGainReg = BbGainReg(True, 1/5)

simCore.InstallReg("RxIir_0", RxIir0Reg)
simCore.InstallReg("RxIir_1", RxIir1Reg)
simCore.InstallReg("RxChannelEst", RxChannelEstReg)
simCore.InstallReg("RxAbs", RxAbsReg)
simCore.InstallReg("RxFir_0", RxFir0Reg)
simCore.InstallReg("RxFir_1", RxFir1Reg)
simCore.InstallReg("RxGain", RxGainReg)
simCore.InstallReg("RxDec", RxDecReg)

"""
Trassmition
"""

simCore.StartFrame()
TxInGate.GenSig(1000, "4QAM")
Scope.Connect("RxDec")
Scope.Plot("constellation")

TxIntReg.Update(False, 5)
TxFirReg.Update(False, np.ones(5))
RxFir1Reg.Update(False, np.ones(5))
RxGainReg.Update(False, 1/5)
RxDecReg.Update(False, 5)

simCore.StartFrame()
TxInGate.GenSig(1000, "4QAM")
Scope.Connect("RxDec")
Scope.Plot("constellation")
