from scipy.io import wavfile
import numpy as np
from mp3 import make_mp3_analysisfb, make_mp3_synthesisfb

from codec import *

# loading the coefficients
data = np.load("h.npy", allow_pickle=True).tolist()
h = data['h'].squeeze()

# defining basic parameters
M = 32 # channels
fs = 44100 # sampling rate
N = 36 # window rate

# calculating analysis/synthesis filters matrices H, G
H = make_mp3_analysisfb(h, M)
G = make_mp3_synthesisfb(h, M)

# plotting analysis results
plot_frequency(H,fs)
fs, wavin = wavfile.read('myfile.wav')
Ytot = coder0(wavin,h,M,N)
plotSubbands(Ytot, M)


xhat, total_stream = MP3codec(wavin, h, M, N)
# writing output file
wavfile.write('output.wav', fs, xhat.astype(np.int16))

# typecasting input and output files
wavin = wavin.astype(np.int64)
xhat = xhat.astype(np.int64)

# syncing input and output signals
L = H.shape[0]
lag = L-M
tmp_wavin, tmp_xhat = wavin[lag:], xhat[:-lag]


# calculating MSE
e = tmp_wavin - tmp_xhat 
mse = np.mean(np.square(e))

# calculate SNR in db
SNR = np.mean(np.square(wavin[lag:])) / mse
SNRdb = 10*np.log10(SNR)
print("SNR = {:.2f}".format(SNRdb))

def calculateCompressionRate(wavin, total_stream, fs, bits_per_sample = 16):
    # calculating input and output data rates
    input_data_rate = fs * bits_per_sample
    output_data_rate = len(total_stream) / (len(wavin) / fs) 

    # calculating compression rate
    compression_rate = input_data_rate / output_data_rate
    return input_data_rate, output_data_rate, compression_rate
    
input_data_rate, output_data_rate, compression_rate = calculateCompressionRate(wavin, total_stream, fs)
print("Compression rate: {:.3f}".format(len(wavin)*16/len(total_stream)))
