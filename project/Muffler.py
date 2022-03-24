# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 13:00:11 2022

@author: prana
"""
import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
from scipy import signal
from operator import add
from operator import mul


def muffler(data_import,fs,cutoff):
    order = 6
    b, a = butter_lowpass(cutoff, fs, order)
    # Plotting the frequency response.
    w, h = freqz(b, a, worN=8000)
    plt.subplot(2, 1, 1)
    plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
    plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
    plt.axvline(cutoff, color='k')
    plt.xlim(0, 0.5*fs)
    plt.title("Lowpass Filter Frequency Response")
    plt.xlabel('Frequency [Hz]')
    plt.grid()

    T = 5.0         # value taken in seconds
    n = int(T * fs) # indicates total samples
    t = np.linspace(0, T, n, endpoint=False)
    t = range(1115759)
    data = data_import

    #Filtering and plotting
    y = butter_lowpass_filter(data, cutoff, fs, order)
    print("y:")
    print(y[2000][1])
    plt.subplot(2, 1, 2)
    plt.plot(t, data, 'b-', label='data')
    plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
    plt.xlabel('Time [sec]')
    plt.grid()
    plt.legend()

    plt.subplots_adjust(hspace=0.35)
    plt.show()
    y = np.array(y).T
    y_1 = y[0:][0]
    y_2 = y[0:][1]
    z_1 = addReverb(y_1,fs)
    #z_2 = addReverb(y_2,fs)

    print(len(z_1))
   # print(len(z_2))
    z = np.stack((z_1,y_2))
    y = np.array(y).T
   # x = y[0:][0]
   # print(len(x))
   # z = np.stack((z,x))
    z = np.array(z).T
    
   #  print(ir_data)
    #ir = np.array(ir_data)
  #%%
    
  
   # print(ir)
   # print("y:")
   # print(y)
   # y=addReverb(y[0:][0], ir[0:][0], 1)


    return z
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def addReverb(data, fs):
  
    #print("change:")
    #print(data) 
    #data = np.fft.fft(data)
    #data = np.fft.fftshift(data)
  
    #data = np.fft.ifft(data)
    #print("here:")
    #print(data)
    #data = data.real
     
    
   # data = np.fft.ifft(np.fft.fftshift(data))
   # data = data.real

    delay = 0.01
    index = round(delay*fs)
    Zero_list = [0]*index
    Zero_list = np.array(Zero_list)
    
    delay_output =np.concatenate((Zero_list, data))
    delay_output = delay_output[0:len(data)]
   
    c = 0;
    out = []
    for i in delay_output:
           out.append(((data[c]+delay_output[c])/2))
           c = c+1 

    return out



def muffler2(data,fs,cutoff):
    length = len(data)
    half_len = int(length/2)
    print(length)

    f = list(range( (-half_len),((half_len+1)), 1))

    c = 0
    for i in f:
        f[c] = f[c]*(fs/length)
        c = c+1
    #print(data)
    input_freq = np.fft.fftshift(np.fft.fft(data))
    #input_freq = np.fft.fft(data)
    low_pass = [0]*len(input_freq)
    c = 0
    #print(len(low_pass))
    #print(len(f))
    for i in low_pass:
        if np.abs(f[c])< cutoff:
            low_pass[c] = 1
        else:
            low_pass[c] = 0
        c=c+1
    
    #input_freq = np.array(input_freq).T
    #print(input_freq)
    c = 0 

    Low_passed_data = [0]*input_freq
    Low_passed_data = list(map(mul,input_freq,low_pass))
    #for i in low_pass:
     #   Low_passed_data.append(input_freq[c]*low_pass[c])
      #  c = c+1

    #Low_passed_data = np.array(Low_passed_data).T
    #print("Low passed:")
    #print(Low_passed_data)
    print("done lowpass")
 
    Low_passed_data = np.fft.ifftshift(Low_passed_data)
    Low_passed_data = np.fft.ifft(Low_passed_data)
    Low_passed_data = Low_passed_data.real
    reverb_data = addReverb(Low_passed_data, fs)

    return reverb_data
            
               