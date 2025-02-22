import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

def ExitError(text):
    print("XxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx")
    print("EXIT ERROR - " + text)
    print("XxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx")   
    exit()
    
def WarningError(text):
    print("XxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx", flush = True)
    print("Warning - " + text, flush = True)
    print("XxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx", flush = True)  
    
def CommonFunHelp():
    print("Common functions:")
    print("-> ExitError(text): prints the input text then exits the program")
    print("-> WarningError(text): prints the input text")
    
def PlotFilterRespons(B, A = 1, name = ""):   
    # Plot magnitude response
    freqs, h = signal.freqz(B, A)
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(freqs, 20 * np.log10(abs(h)))
    plt.title(name + " Magnitude Response")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Magnitude [dB]")
    plt.grid()
    # Plot phase response
    plt.subplot(1, 2, 2)
    plt.plot(freqs, np.angle(h))
    plt.title(name + " Phase Response")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Phase [radians]")
    plt.grid()
    plt.tight_layout()
    plt.show()
    
def CommonHelp():
    print("Callable common functions:")
    print("-> ExitError(txt): prints the text in error format then exit the simulation")
    print("-> WarningError(txt): prints the text in error format")
    print("-> PlotFilterRespons(sampleRate, B, A = 1, name = None): plot filter response, B is the numerator coeff and A the denominator")