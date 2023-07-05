from src.modules.utils import *
import numpy as np
from scipy.io import wavfile

def process(**kwargs):
    file = kwargs['file']
    rate, file = wavfile.read(file)
    subbands = kwargs['subbands']
    samples = kwargs['samples']
    filter = np.load('../res/config/h.npy', allow_pickle=True).tolist()
    filter = filter['h'].squeeze()
    
    Y_total = Utils.encode(file, filter, subbands, samples)
    return Utils.plot_subbands(Y_total, subbands, rate)