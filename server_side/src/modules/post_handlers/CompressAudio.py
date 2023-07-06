from src.modules.utils import Utils
import numpy as np
from scipy.io import wavfile

def process(**kwargs):
    file = kwargs['file']
    subbands = kwargs['subbands']

    Utils.compress_mp3(file, subbands)
    return {
        'status': 'success'
    }