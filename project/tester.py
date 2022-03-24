# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 11:42:41 2022

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
fs = 30000
rand = random.random()
delay = 0.003 * random.random()
index = round(delay*fs)
zeros = [0]*index
print(zeros)
input_nums= list(range(0,15))
added = zeros+input_nums
print(added)
list_1 = list((range(5)))
list_2 = list(range(7,12))
print(list_1)
print(list_2)
added = list(map(add,list_1,list_2))
print(added)
