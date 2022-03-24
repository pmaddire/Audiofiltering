# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 15:10:09 2022

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
from Chorus import *
from operator import add
from Ampfreqrange import *

def linearpitchenvelope(input_data,fs,attack,decay,sustain,release):# %percentages for attack,decay,sustain,release added up to 1.
    length = len(input_data)
    T = (length)/fs 
    attacktime = attack * T * fs
    decaytime = attacktime + (decay * T * fs)
    sustaintime = (T - (release * T)) * fs
    
    output = [0]*length 
    
    tcounter = 0
    #attack 
    curr = attacktime 
    x = list(range(length))
    
    y = [0]*len(x)
    g = [0]*len(x)
    
    while tcounter <= curr:
        ncount = round((tcounter**2)/(2*curr)+curr/2)
        y[tcounter] = ncount 
        output[tcounter] = input_data[ncount]
        tcounter = tcounter + 1
    
    #decay
    
    prevcur = curr 
    tcounter = prevcur
    curr = decaytime
    
    while tcounter <= curr: 
        
        t = round(tcounter - prevcur)
        dur = round(curr-prevcur)
        dsus = (1-sustain)
        
        dn = (1 - (dsus)*t/(2*dur))*t
        ncount = round(prevcur + dn)
        tcounter = round(tcounter)
        
        y[tcounter] = ncount
        output[tcounter] = input_data[ncount]
        tcounter = tcounter + 1
    
    #sustain 
    
    prevncount = ncount
    prevcur = curr
    tcounter = prevcur
    curr = sustaintime
    
    while tcounter <= curr: 
        t = round(tcounter-prevcur)
        ncount = round(sustain*t+prevncount)
        tcounter = round(tcounter)
        
        y[tcounter] = ncount
        output[tcounter] = input_data[ncount]
        tcounter = tcounter+1
    
    #release 
    
    prevncount = ncount
    prevcur = curr
    tcounter = prevcur
    curr = fs    
    
#    while tcounter <= curr:
#        t = round(tcounter - prevcur)
#        dur = round(curr - prevcur)
#
#        dn = (sustain - (sustain)*t/(2*dur))*t
#        ncount = round(prevncount + dn)
#        
#        tcounter = round(tcounter)
#        y[tcounter] = ncount
#        if ncount > length :
#            output[tcounter] = 0
#        else:
#            output[tcounter] = input_data[ncount]
#        tcounter = tcounter+1
   
 
    
    while tcounter <= curr: 
        
        t = round(tcounter - prevcur)
        dur = round(curr-prevcur)
        dsus = (1-sustain)
        
        dn = (1 - (dsus)*t/(2*dur))*t
        ncount = round(prevcur + dn)
        tcounter = round(tcounter)
        
        y[tcounter] = ncount
        output[tcounter] = input_data[ncount]
        tcounter = tcounter + 1 
        
        if ncount > length:
            output[tcounter] = 0
   
    
   
    
    return output
    
    
    
    
    
    