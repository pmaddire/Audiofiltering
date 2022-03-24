# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 12:57:12 2022

@author: prana
"""

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
import numpy as np

def ampfreqrange(input_data,fs,low,high,multiplier):
    
    length = len(input_data)
    half_len = int(length/2)
    print(length)

    f = list(range( (-half_len),((half_len+1)), 1))

    c = 0
    for i in f:
        f[c] = f[c]*(fs/length)
        c = c+1
    #print(data)
    input_freq =np.fft.fftshift(np.fft.fft(input_data))
    Amp_filter = [0]*len(input_freq)
    c = 0
    for i in input_freq:
        if(low < np.abs(f[c])) and (np.abs(f[c]) < high): 
         
           Amp_filter[c] = multiplier
        else:
            Amp_filter[c] = 1
        c = c+1
    Amp_filter_data = [0]*input_freq
    Amp_filter_data = list(map(mul,Amp_filter,input_freq))
    
    
 
    Amp_filter_data = np.fft.ifftshift(Amp_filter_data)
    Amp_filter_data = np.fft.ifft(Amp_filter_data)
    Amp_filter_data = Amp_filter_data.real
    
    return Amp_filter_data
 
 

    
    

