import numpy as np
import scipy.signal as signal
from BlocksBank.BaseBlocks import *
from BlocksBank.OtherBlocks import *
from BlocksBank.ComplexBlocks import *
from BlocksBank.CommonFun import *

simCore = SimCore()
simCore.DBG(1, "W", 1)

Scope = Analyzer("Scope_0", simCore)

"""
Build system
"""

TxVec = [Tx(simCore, 0), Tx(simCore, 1)]
RxVec = [Rx(simCore, 0), Rx(simCore, 1)]
Analog = Analog(simCore, 0)

"""
Registers and configurations
"""

Analog.GetReg("Analog0AwgnReg").Update(False, 0.1)
Analog.GetReg("Analog0SdrReg").Update(True, 600000, 1500000000, 1500000000, "slow_attack", -50)

preambleSeq = np.array([10, 10, -10, -10, 10, 10, -10, -10])
pulse0 = np.array([1, 1, 1, 1, 1, 0, -1, -1, -1, -1, -1])
pulse1 = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

TxVec[0].GetReg("Tx0IntReg").Update(False, 11)
TxVec[0].GetReg("Tx0GainReg").Update(False, 1)
TxVec[0].GetReg("Tx0Fir0Reg").Update(False, pulse0)
TxVec[0].GetReg("Tx0PreambleReg").Update(False, preambleSeq)

RxVec[0].GetReg("Rx0ChannelEstReg").Update(False, 2 * preambleSeq)
RxVec[0].GetReg("Rx0Fir1Reg").Update(False, pulse0)
RxVec[0].GetReg("Rx0GainReg").Update(False, 1/np.sum(pulse0**2))
RxVec[0].GetReg("Rx0DecReg").Update(False, 11)
RxVec[0].GetReg("Rx0DetectorReg").Update(False, "16QAM")

TxVec[1].GetReg("Tx1IntReg").Update(False, 11)
TxVec[1].GetReg("Tx1Fir0Reg").Update(False, pulse1)
TxVec[1].GetReg("Tx1PreambleReg").Update(False, preambleSeq)

RxVec[1].GetReg("Rx1ChannelEstReg").Update(False, 2 * preambleSeq)
RxVec[1].GetReg("Rx1Fir1Reg").Update(False, pulse1)
RxVec[1].GetReg("Rx1GainReg").Update(False, 1/1/np.sum(pulse1**2))
RxVec[1].GetReg("Rx1DecReg").Update(False, 11)
RxVec[1].GetReg("Rx1DetectorReg").Update(False, "8PSK")

"""
Simulation
"""

simCore.StartFrame()
simCore.GetBlock("Tx0InGate").GenSig(10000, "16QAM")
simCore.GetBlock("Tx1InGate").GenSig(10000, "8PSK")
out0 = simCore.GetBlock("Tx0Fir_1").mOutput
out1 = simCore.GetBlock("Tx1Fir_1").mOutput
Analog.mInput = out0 + out1
Analog.CallProccess()
RxVec[0].mInput = Analog.mOutput
RxVec[1].mInput = Analog.mOutput
RxVec[0].CallProccess()
RxVec[1].CallProccess()
Scope.Connect("Analog0Sdr")
Scope.Plot("fft", 10000)
Scope.Connect("Rx0Dec")
Scope.Plot("constellation")
Scope.Connect("Rx1Dec")
Scope.Plot("constellation")
