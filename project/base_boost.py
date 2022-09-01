from pydub import AudioSegment
from os import listdir
import numpy as np
import math

def start_bass(attenuate_db,accentuate_db,src,save_src):

    song_dir = src
    attenuate_db = 0
    accentuate_db = 5
    print('filtering...')
    
    sample = AudioSegment.from_wav(src)
    filtered = sample.low_pass_filter(bass_line_freq(sample.get_array_of_samples()))

    combined = (sample - attenuate_db).overlay(filtered + accentuate_db)
    combined.export(save_src, format="wav")
    print("file saved")
def bass_line_freq(track):
    sample_track = list(track)

    # c-value
    est_mean = np.mean(sample_track)

    # a-value
    est_std = 3 * np.std(sample_track) / (math.sqrt(2))

    bass_factor = int(round((est_std - est_mean) * 0.005))

    return bass_factor


