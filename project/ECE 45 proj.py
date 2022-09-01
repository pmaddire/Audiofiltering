# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 22:18:59 2022

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
from LinearPitchEnvelope import *
from base_boost import *
from pydub import AudioSegment

fx = (
    AudioEffectsChain()
    .reverb()
   
)
pg.init()
pg.mixer.init()
#wav = wave.open("src_Strong_Bassline.wav","r")

#raw = wav.readframes(-1)
#raw = np.frombuffer(raw,"Int16")

#if wav.getnchannels()==2:
#    print("Stereo Files are not supported. Use Mono Files")
    


print("Audio editor start...")
src = input("Please Enter name of wav file that will be edited. Example: src_Strong_Bassline.wav: ")
save_process = 1



print("Filter list:")
print("------------------------")
print("1. Muffle Filter")
print("2. Chorus Filter")
print("3. Amplify frequency range")
print("4. Linear Pitch Envelope")
print("5. Bass Boost")
filter_choose = input("Enter desired filter number: ")
save_src = input("Enter file name for edited sound Example: Chorus_bassline.wav: ")
filter_choose = int(filter_choose)
print(filter_choose)
print(src)
print(save_src)


    
    
    
samplerate,data = wavfile.read(src)
#data_plot = np.frombuffer(data,"Int16")
#print(samplerate-400)
#print("top")
length = len(data)
#print("Length =",)
#print(length)
data = np.array(data.T)
data_1 = data[0:][0]
data_2 = data[0:][1]
#print(data_1)


fft_spectrum = np.fft.rfft(data_1)
freq = np.fft.rfftfreq(data_1.size, d=1./samplerate)
fft_spectrum_abs = np.abs(fft_spectrum)
plt.plot(freq[:15000], fft_spectrum_abs[:15000])
plt.xlabel("frequency, Hz")
plt.ylabel("Amplitude, units")
plt.show()







print("choosing filter")
if filter_choose == 1:
#muffle filter
    print("start muffling")
    cutoff = int(input("What would you like the cutoff frequency to be?: "))
    muffled = muffler2(data_1,samplerate*2,cutoff)
#print("out")
#print("is muff")
    muffled_2 = muffler2(data_2,samplerate*2,cutoff)
#print("out")
    data_0 = np.stack((muffled,muffled_2),axis=1)
#print("next")
elif filter_choose == 2:
#chorus Filter def chor(input_data,fs,cutoff)
    cutoff = int(input("What would you like the cutoff frequency (frequencies to amp) to be?: "))
    chor_1 = chor(data_1, samplerate*2,cutoff)
    #chor_2 = chor(data_2, samplerate*2,cutoff)
    data_0 = np.stack((chor_1,chor_1),axis=1)

elif filter_choose == 3:
    
    #def ampfreqrange(input_data,fs,low,high,multiplier):
    low = int(input("What would you like the low frequency to be?: "))
    high = int(input("What would you like the High frequency to be?: "))
    multiplier = float(input("What would you like the multiplier to be?: "))
    ampfreq_1 = ampfreqrange(data_1, samplerate, low, high, multiplier)
    ampfreq_2 = ampfreqrange(data_1, samplerate, low, high, multiplier)
    data_0 = np.stack((ampfreq_1,ampfreq_2),axis=1)

elif filter_choose == 4:
    
    #def LinearPitchEnvelope(input_data,fs,attack,decay,sustain,release):# %percentages for attack,decay,sustain,release added up to 1.
    
    attack = float(input("What would you like the attack percentage to be? Example :25=25%:  "))/100
    decay = float(input("What would you like the decay percentage to be? Example :25=25%:  "))/100
    sustain = float(input("What would you like the sustain percentage to be? Example :25=25%:  "))/100
    release = float(input("What would you like the release percentage to be? Example :25=25%:  "))/100
    
    linearPitch_1 = linearpitchenvelope(data_1,samplerate,attack,decay,sustain,release)
    linearPitch_2 = linearpitchenvelope(data_2,samplerate,attack,decay,sustain,release)

    data_0 = np.stack((linearPitch_1,linearPitch_2),axis=1)
    
elif filter_choose == 5:
    attenuate_db = int(input("Attenuate_db:"))
    accentuate_db = int(input("Accentuate_db:"))
    start_bass(attenuate_db,accentuate_db,src,save_src)
    save_process = 0
    quit()
plt.clf()



#print(data_0)

#muffled = fx(muffled)
#print (muffled)
data_0 = np.array(data_0).astype(np.int16)
#print(data_0)


#print("back")
#print(data_plot)
sound = pg.sndarray.make_sound(data_0.copy())
#sound.play()



#sampling_rate = 44100 
#frequency = 440 #(Hz)
#duration = 1.5 #(s)
#frames = int(duration*sampling_rate)
#arr = np.cos(2*np.pi*frequency*np.linspace(0,duration,frames))
#sound = np.asarray([132767*arr,32767*arr]).T.astype(np.int16)
#sound = pg.sndarray.make_sound(sound.copy())
#sound.play()
data_01 = np.array(data_0).T
data_01 = data_01[0:][0]

fft_spectrum = np.fft.rfft(data_01)
freq = np.fft.rfftfreq(data_1.size, d=1./samplerate)
fft_spectrum_abs = np.abs(fft_spectrum)
plt.plot(freq[:15000], fft_spectrum_abs[:15000])
plt.xlabel("frequency, Hz")
plt.ylabel("Amplitude, units")
plt.show()

next_plot = input("Hit enter to show next plot: ")
plt.clf()

t = list(range(len(data_1)))
data_0 = np.array(data_0).T
print("plotting")
plt.subplot(2, 1, 2)
plt.plot(t, data_1, 'b-', label='data')
plt.plot(t, data_0[0:][0], 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

print("saving file")



sfile = wave.open(save_src,'w')
sfile.setframerate(samplerate)
sfile.setnchannels(2)
sfile.setsampwidth(2)
sfile.writeframesraw(sound)
sfile.close()











#plt.title("Sound Wave")
#plt.plot(t, data[0:300])

#plt.title ("Waveform of Wave File")

#plt.plot(data,color ="blue")
#plt.ylabel("Amplitude")
#plt.show()