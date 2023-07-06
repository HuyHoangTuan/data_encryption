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
    temp_file = f'../res/temp/temp_plot_image_{current_time}.wav'
    with open(temp_file, 'wb') as f:
        f.write(file.stream.read())

    response_stream = 'test'
    try:
        response_stream = Utils.process_plot_subbands(temp_file, bit_rate)
        os.remove(temp_file)
    except:
        print('Error in process plot image!')
        os.remove(temp_file)
    
    return response_stream