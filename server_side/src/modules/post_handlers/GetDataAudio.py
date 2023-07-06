from src.modules.utils import Utils
import numpy as np
from scipy.io import wavfile

def process(**kwargs):
    file = kwargs['file']
    subbands = kwargs['subbands']
    return {
        'compression_rate': 0,
    }
