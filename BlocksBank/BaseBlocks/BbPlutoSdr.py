import numpy as np
import adi
from ..CommonFun import *
from .BaseBlock import BaseBlock



class BbPlutoSdr(BaseBlock):

    def __init__(self, name, simCore):
        super().__init__(name, simCore)
        self.mType = "BbPlutoSdr"
        self.mSdr = None
        self.mSampleRate = None

    def Proccess(self):
        self.mInput = self.mInput + 0j
        normalization = np.max(np.abs(self.mInput))
        normalizedInput = self.mInput * 2 ** 14 / (normalization + 1e-6)
        buffer_size = 2 ** int(np.ceil(np.log2(len(self.mInput))))
        self.mSdr.rx_buffer_size = buffer_size
        self.mSdr.tx_cyclic_buffer = True
        if self.mSimCore.DBG(1):
            print(self.mName + " - Transmission started")
        self.mSdr.tx(normalizedInput)
        self.mSdr.rx_destroy_buffer()
        for i in range(3):
            self.mSdr.rx()
        recievedData = self.mSdr.rx()
        self.mSdr.tx_destroy_buffer()
        if self.mSimCore.DBG(1):
            print(self.mName + " - Transmission ended")
        self.mOutput = recievedData[0:len(self.mInput)]
           
    def LoadConfig(self, register):
        if self.mSdr is None:
            self.mSdr = adi.Pluto("ip:192.168.2.1")
        if register.mSampleRate < 530000:
            ExitError(self.mName + " - Hardware support sampleRate above 530000 -> change sample rate")
        self.mSdr.sample_rate = int(register.mSampleRate)
        if register.mRxLoFreq < 325000000 or register.mRxLoFreq > 3800000000:
            ExitError(self.mName + " - Hardware support Rx LO frequency between 325 MHz and 3.8 GHz -> change RX LO freq")
        self.mSdr.rx_lo = int(register.mRxLoFreq)
        if register.mTxLoFreq < 325000000 or register.mTxLoFreq > 3800000000:
            ExitError(self.mName + " - Hardware support Tx LO frequency between 325 MHz and 3.8 GHz -> change TX LO freq")
        self.mSdr.tx_lo = int(register.mTxLoFreq)
        if register.mTxGain < -89 or register.mTxGain > 0:
            ExitError(self.mName + " - Hardware support Tx gain  between -90 and 0 -> change TX gain")
        self.mSdr.tx_hardwaregain_chan0 = int(register.mTxGain)
        if type(register.mRxGain) == str:
            if register.mRxGain != "slow_attack" and register.mRxGain != "fast_attack":
                ExitError(self.mName + " - Chosen RX gain mode is not valid -> change value, slow_attack or fast attack")
            self.mSdr.gain_control_mode_chan0 = register.mRxGain
        else:
            if register.mRxGain < 0 or register.mRxGain > 70:
                ExitError(self.mName + " - Hardware support Rx gain  between 0 and 70 -> change RX gain")
            self.mSdr.gain_control_mode_chan0 = "manual"
            self.mSdr.rx_hardwaregain_chan0 = int(register.mRxGain)
        self.mSdr.tx_rf_bandwidth = int(self.mSdr.sample_rate / 2)
        self.mSdr.rx_rf_bandwidth = int(self.mSdr.sample_rate / 2)
        
    def Help(self):
        print("BbPlutoSdr block Proccess:")
        print(" -> Simple linear amplifier")  
        print("BbPlutoSdr register(bypass, sampleRate, rxLoFreq, txLoFreq, rxGain, txGain):")
        print(" -> bypass: if True, connects input directly to the output")
        print(" -> sampleRate: ADC and DAC sample rate")
        print(" -> rxLoFreq: Rx LO frequency (from 325 MHz to 3.8 GHz)") 
        print(" -> txLoFreq: Tx LO frequency (from 325 MHz to 3.8 GHz)") 
        print(" -> rxGain: Rx gain: value (0 to 70) or mode (slow_attack or fast_attack)")   
        print(" -> txGain: Tx gain - value from -90 to 0 (refered to maximum TX power - 8dBm)") 
        print(" -> txBandwidth: Tx Analog filter bandwidth, not configurable yet, needs to be changed") 
        print(" -> rxBandwidth: Rx Analog filter bandwidth, not configurable yet, needs to be changed")        
        
class BbPlutoSdrReg():

    def __init__(self, bypass, sampleRate, rxLoFreq, txLoFreq, rxGain, txGain):
        self.mType = "BbPlutoSdrReg"
        self.mByPass = bypass
        self.mSampleRate = sampleRate
        self.mRxLoFreq = rxLoFreq
        self.mTxLoFreq = txLoFreq
        self.mRxGain = rxGain
        self.mTxGain = txGain
        
    def Update(self, bypass, sampleRate, rxLoFreq, txLoFreq, rxGain, txGain):
        self.mByPass = bypass
        self.mSampleRate = sampleRate
        self.mRxLoFreq = rxLoFreq
        self.mTxLoFreq = txLoFreq
        self.mRxGain = rxGain
        self.mTxGain = txGain