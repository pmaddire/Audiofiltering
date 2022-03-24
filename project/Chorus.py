# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 15:52:22 2022

@author: prana
"""
import pygame as pg
import numpy as np
import matplotlib.pyplot as plt
from os import path
from pydub import AudioSegment 
from scipy.io import wavfile
from scipy import signal
import wave 
from Muffler import *
from pysndfx import AudioEffectsChain
import random
from operator import add
from operator import mul

def chor(input_data,fs,cutoff):
    
    length = len(input_data)
    half_len = int(length/2)
    print(length)

    f = list(range( (-half_len),((half_len+1)), 1))

    c = 0
    for i in f:
        f[c] = f[c]*(fs/length)
        c = c+1
    #print(data)
    input_freq = np.fft.fftshift(np.fft.fft(input_data))
    low_Amp_filter = [0]*len(input_freq)
    c = 0
    #print(len(low_pass))
    #print(len(f))
    for i in low_Amp_filter:
        if np.abs(f[c])< cutoff:
            low_Amp_filter[c] = 1.25
        else:
            low_Amp_filter[c] = 1.00
        c=c+1
    
    #input_freq = np.array(input_freq).T
    #print(input_freq)
    #c = 0 
    Low_Amp_data = [0]*input_freq
    Low_Amp_data = list(map(mul,low_Amp_filter,input_freq))
    #for i in low_Amp_filter:
     #   Low_Amp_data.append(input_freq[c]*low_Amp_filter[c])
     #   c = c+1

    #Low_passed_data = np.array(Low_passed_data).T
    #print("Low passed:")
    #print(Low_passed_data)
    print("low_Amp_filter done")
 
    Low_Amp_data = np.fft.ifftshift(Low_Amp_data)
    Low_Amp_data = np.fft.ifft(Low_Amp_data)
    Low_Amp_data = Low_Amp_data.real
    
    c = 0
    out = [0]*len(Low_Amp_data)
    while c <= 100:
        print("iteration",c)
        rand = random.random()
        delay = 0.003 * rand
        index = round(delay*fs)
        zeros = [0]*index
        delay_output =np.concatenate((zeros, Low_Amp_data))
        delay_output = delay_output[0:len(Low_Amp_data)]
       # x = 0;
       # for i in delay_output:
        #   out[x]= ((out[x]+delay_output[x]))
         #  x = x+1 
        c = c+1
        out = list(map(add,out,delay_output))

    
    c = 0
    for i in out:
       out[c]= (out[c]/100)
       c = c+1
 

    
    


    return out
                
    
