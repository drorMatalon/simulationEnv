import numpy as np
import scipy.signal as signal
from BlocksBank.BaseBlocks import *
from BlocksBank.OtherBlocks import *
from BlocksBank.Modulators import *
from BlocksBank.CommonFun import *

simCore = SimCore()
simCore.DBG(1, "W", 0)

Scope = Analyzer("Scope_0", simCore)

"""
TX chain: in gate -> interpulator -> FIR (for pulse shaping) -> gain -> Analog
"""

TxInGate = InGate("TxInGate_0", simCore)
TxInt = BbInt("TxInterpulator", simCore)
TxFir = BbFir("TxFir", simCore)
TxMixer = BbMixer("TxMixer", simCore)
simCore.Connect("TxInGate_0", "TxInterpulator", "TxFir", "TxMixer")

"""
Rx chain: Analog -> IIR0 (Notched) -> IIR1 (Notched) -> FIR (Matched filter) -> Decimator -> gain
"""

RxIir = BbIir("RxIir", simCore)
RxAbs = BbAbs("RxAbs", simCore)
RxFir = BbFir("RxFir_0", simCore)
RxFir = BbFir("RxFir_1", simCore)
RxDec = BbDec("RxDec", simCore)
RxGain = BbGain("RxGain", simCore)
simCore.Connect("RxIir", "RxAbs", "RxFir_0", "RxFir_1", "RxDec", "RxGain")

"""
Analog: Awgn or Sdr, disable one of them!
"""

Awgn = BbAwgn("Awgn", simCore)
Sdr = BbPlutoSdr("Sdr", simCore)
simCore.Connect("TxMixer", "Awgn", "Sdr", "RxIir")

"""
Registers generation and installation
"""

n = np.linspace(0, 59, 60)
gaussian = np.exp(-(n-25)**2/(2 * (12**2)))

TxIntReg = BbIntReg(False, 50)
TxFirReg = BbFirReg(False, gaussian)
TxMixerReg = BbMixerReg(False, 100, 500)

simCore.InstallReg("TxInterpulator", TxIntReg)
simCore.InstallReg("TxFir", TxFirReg)
simCore.InstallReg("TxMixer", TxMixerReg)

AwgnReg = BbAwgnReg(False, 1)
SdrReg = BbPlutoSdrReg(True, 600000, 1000000000, 1000000000, "slow_attack", -40)

simCore.InstallReg("Awgn", AwgnReg)
simCore.InstallReg("Sdr", SdrReg)

RxIirReg = BbIirReg(False, [1, -2 * np.cos(0), 1], [1, -2 * 0.95 * np.cos(0), 0.95 * 0.95])
RxAbsReg = BbAbsReg(False, False)
RxFir0Reg = BbFirReg(False, signal.firwin(16, 150, fs=500, window="hamming"))
RxFir1Reg = BbFirReg(False, gaussian)
RxDecReg = BbDecReg(True, 50)
RxGainReg = BbGainReg(True, 3/400)

simCore.InstallReg("RxIir", RxIirReg)
simCore.InstallReg("RxAbs", RxAbsReg)
simCore.InstallReg("RxFir_0", RxFir0Reg)
simCore.InstallReg("RxFir_1", RxFir1Reg)
simCore.InstallReg("RxDec", RxDecReg)
simCore.InstallReg("RxGain", RxGainReg)

"""
Trassmition
"""

simCore.StartFrame()
TxInGate.GetSamples([0, 0, 10, 10, 5, 5, 0, 0, 2, 8, 6, 8])
Scope.Connect("RxFir_0")
Scope.Plot("fft")
Scope.Connect("RxDec")
Scope.Plot("power")