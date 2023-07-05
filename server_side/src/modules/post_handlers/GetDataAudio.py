from src.modules.utils import Utils
import numpy as np
from scipy.io import wavfile

def process(**kwargs):
    file = kwargs['file']
    rate, file = wavfile.read(file)
    subbands = kwargs['subbands']
    samples = kwargs['samples']
    filter = np.load('../res/config/h.npy', allow_pickle=True).tolist()
    filter = filter['h'].squeeze()
    
    x_hat, total_stream = Utils.compress_mp3(file, filter, subbands, samples)
    
    wav = file.astype(np.int64)
    x_hat = x_hat.astype(np.int64)
    input_data_rate, output_data_rate, compression_rate = Utils.calculate_compression_data(wav, total_stream, rate)
    return {
        'compression_rate': compression_rate,
    }
