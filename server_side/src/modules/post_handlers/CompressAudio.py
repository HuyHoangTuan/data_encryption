from src.modules.utils import Utils
import numpy as np
from scipy.io import wavfile
import time
import os
import uuid

def process(**kwargs):
    file = kwargs['file']
    bit_rate = kwargs['bit_rate']

    current_time = uuid.uuid1()
    temp_file = f'../res/temp/temp_compress_audio_{current_time}.wav'
    save_file = f'../res/output/sound_{current_time}.mp3'
    if(os.path.exists(save_file)):
        os.remove(save_file)
    with open(temp_file, 'wb') as f:
        f.write(file.stream.read())

    response = {}
    try:
        object_mp3 = Utils.compress_mp3_with_custom_bit_rate(temp_file, bit_rate)
        for i in range(0, object_mp3['len']):
            params = object_mp3['params'][i]
            subband_bit_allocation = object_mp3['subband_bit_allocation'][i]
            scfindices = object_mp3['scfindices'][i]
            subband_samples_quantized = object_mp3['subband_samples_quantized'][i]
            Utils.save_mp3(save_file, params, subband_bit_allocation, scfindices, subband_samples_quantized)
            
        response['compression_rate_by_bit_rate'] = object_mp3['compression_rate_by_bit_rate']
        response['compression_rate_by_file_size'] = os.stat(temp_file).st_size / os.stat(save_file).st_size
        response['file_size'] = f'{os.stat(temp_file).st_size}/{os.stat(save_file).st_size}'
        
        os.remove(temp_file)
    except:
        print('Error in process Compress!')
        os.remove(temp_file)
    
    return response