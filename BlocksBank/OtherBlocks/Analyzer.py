import numpy as np
import matplotlib.pyplot as plt
from ..CommonFun import *

class Analyzer:

    def __init__(self, name, simCore):
        self.mName = name
        self.mSimCore = simCore
        self.mSimCore.RegisterBlock(self)      
        self.mType = "Analyzer"
        self.mConnectDone = False
        self.mAnalyzedBlock = None
        self.mInput = None
        self.mOutput = None
    
    def Connect(self, blockName):
        self.mAnalyzedBlock = self.mSimCore.GetBlock(blockName)
        self.mConnectDone = True
        
    def Plot(self, mode = "power", fs = 0):
        if not self.mConnectDone:
            ExitError("Analyzer - no connected block -> Connect block first")
        self.mInput = self.mAnalyzedBlock.mInput  
        self.mOutput = self.mAnalyzedBlock.mOutput          
        if self.mInput is None:
            ExitError(self.mName + " - no input error -> remmember to trassmit first or check data path")
        if self.mOutput is None and self.mAnalyzedBlock.mType != "InGate":
            ExitError(self.mName + " - no output error -> remmember to trassmit first or check data path")  
        if mode == "power":
            self.PlotPower()
        elif mode == "constellation":
            self.PlotConstellation()   
        elif mode == "fft":  
            self.PlotFft(fs)
        else:
            ExitError(self.mName + " - plot mode is not valid -> choose power, fft or constellation")  

    def PlotPower(self):    
        #create figure
        fig, plots = plt.subplots(2, 2)
        #input signals preperation
        inN = len(self.mInput)
        inTime = np.linspace(0, inN - 1, inN)
        inRealPart = np.array(self.mInput).real
        inImagPart = np.array(self.mInput).imag
        #input plots
        plots[0, 0].plot(inTime, inRealPart)
        plots[0, 0].set_title(self.mAnalyzedBlock.mName + " input real amplitude")
        plots[0, 0].set_xlabel("time")
        plots[1, 0].plot(inTime, inImagPart)
        plots[1, 0].set_title(self.mAnalyzedBlock.mName + " input imag amplitude")
        plots[1, 0].set_xlabel("time")
        if self.mAnalyzedBlock.mType != "InGate":
            #output signals preperation        
            outN = len(self.mOutput)
            outTime = np.linspace(0, outN - 1, outN)
            outRealPart = np.array(self.mOutput).real
            outImagPart = np.array(self.mOutput).imag
            #output plots
            plots[0, 1].plot(outTime, outRealPart)
            plots[0, 1].set_title(self.mAnalyzedBlock.mName + " output real amplitude")
            plots[0, 1].set_xlabel("time")
            plots[1, 1].plot(outTime, outImagPart)
            plots[1, 1].set_title(self.mAnalyzedBlock.mName + " output imag amplitude")
            plots[1, 1].set_xlabel("time")
        #plot figure
        plt.tight_layout()
        plt.show()

    def PlotConstellation(self):
        output = None
        if self.mAnalyzedBlock.mType == "InGate":
            output = np.array(self.mInput).astype(complex)
        else:
            output = np.array(self.mOutput).astype(complex)
        I = output.real 
        Q = output.imag 
        plt.scatter(I, Q, alpha=0.5)
        plt.title(self.mAnalyzedBlock.mName + " output constellation")
        plt.xlabel("In-Phase (I)")
        plt.ylabel("Quadrature (Q)")
        plt.grid(True)
        plt.show()

    def PlotFft(self, fs):
        #create figure
        fig, plots = plt.subplots(2, 2)
        #input signals prepertion
        inN = len(self.mInput)
        inTime = np.linspace(0, inN - 1, inN)
        inFreq = np.fft.fftfreq(inN) * 2 * np.pi
        if fs > 0:
            inFreq = np.fft.fftfreq(inN, 1/fs)
        fftInSignal = np.abs(np.fft.fft(self.mInput))
        # Input plots
        plots[0, 0].semilogy(inFreq, np.abs(fftInSignal))
        plots[0, 0].set_title(self.mAnalyzedBlock.mName + " input FFT Magnitude")
        plots[0, 0].set_xlabel("frequency")
        plots[0, 0].set_ylabel("Magnitude")
        plots[0, 0].grid()
        plots[1, 0].plot(inFreq, np.angle(fftInSignal))
        plots[1, 0].set_title(self.mAnalyzedBlock.mName + " input FFT Phase")
        plots[1, 0].set_xlabel("frequency")
        plots[1, 0].set_ylabel("Phase")
        plots[1, 0].grid()
        if self.mAnalyzedBlock.mType != "InGate":
            #output signals preperation        
            outN = len(self.mOutput)
            outTime = np.linspace(0, outN - 1, outN)
            outFreq = np.fft.fftfreq(outN) * 2 * np.pi
            if fs > 0:
                outFreq = np.fft.fftfreq(outN, 1/fs)
            fftOutSignal = np.fft.fft(self.mOutput)        
            # Output plots
            plots[0, 1].semilogy(outFreq, np.abs(fftOutSignal))
            plots[0, 1].set_title(self.mAnalyzedBlock.mName + " output FFT Magnitude")
            plots[0, 1].set_xlabel("frequency")
            plots[0, 1].set_ylabel("Magnitude")
            plots[0, 1].grid()
            plots[1, 1].plot(outFreq, np.angle(fftOutSignal))
            plots[1, 1].set_title(self.mAnalyzedBlock.mName + " output FFT Phase")
            plots[1, 1].set_xlabel("frequency")
            plots[1, 1].set_ylabel("Phase")
            plots[1, 1].grid()
        #plot figure
        plt.tight_layout()
        plt.show()

    def Help(self):
        print("Analyzer block interface:")
        print("Constructor(name, simCore):")
        print("-> name - block name to print in log")
        print("-> simCore - simulation core")
        print("Methods:")
        print("-> Connect(block name) - connect blocks to analyze")
        print("-> Plot(mode = \"power\") - plots the connected block data: \"power\" = real and imagionary parts over time, \"constellation\" = real imaginary constellation, \"fft\" = fft abs + phase")