import numpy as np
import matplotlib.pyplot as plt
import io

def compress_mp3(wav_file, num_subbands):
    N = num_subbands
    from src.modules.utils.calc_qmfsubband import pqmf_analysis_filterbank_fast, pqmf_synthesis_filterbank_fast, optimfuncQMF, pqmf_analysis_filterbank, pqmf_synthesis_filterbank
    from src.modules.utils.synthesis_matrix import hs2Fs3d_fast
    from src.modules.utils.analysis_matrix import ha2Fa3d_fast
    import scipy as sp
    import wave
    import struct
    import math
    
    # x0 = 16 * sp.ones(4 * N)
    # xmin = minimize(optimfuncQMF,x0, args=(N,), method='SLSQP')
    # sp.savetxt("../res/config/QMFcoeff.txt", xmin.x)

    qmfwin=np.loadtxt('../res/config/qmf.dat')
    qmfwin = np.concatenate((qmfwin,np.flipud(qmfwin)))

    wf = wave.open(wav_file,'rb')
    
    n_channel=wf.getnchannels()
    bytes=wf.getsampwidth()
    rate=wf.getframerate()
    length=wf.getnframes()

    # store wav file
    wfw = wave.open('../res/output/test_rek.wav', 'wb')
    wfw.setnchannels(n_channel)
    wfw.setsampwidth(2)
    wfw.setframerate(rate)

    overlap=int(len(qmfwin)/N)
    # overlap = int(N/3)
    blockmemory=np.zeros((overlap,N))
    blockmemorysyn=np.zeros((overlap,N))

    Fa = ha2Fa3d_fast(qmfwin, N)
    Fs = hs2Fs3d_fast(qmfwin, N)

    print(f'Start QMF: L: {length} -- B: {int(length/N)}')
    for m in range(int(length/N)):
        print("Block number: ", m)
        
        #Analysis:
        data=wf.readframes(N)
        x = (struct.unpack( 'h' * N, data ))
        y = pqmf_analysis_filterbank_fast(x,Fa, N, blockmemory, overlap)
        # y = pqmf_analysis_filterbank(x,Fa, N)
        #plt.plot(y)
        #plt.show(block=False)

        #Synthesis:
        xrek = pqmf_synthesis_filterbank_fast(y,Fs, N, blockmemorysyn, overlap)
        # xrek = pqmf_synthesis_filterbank(y,Fs, N)  
        #write with 2 Bytes per sample:
        #Convert to short ints:
        
        xrek=np.array(xrek[:N] ,dtype='int16')
        data=struct.pack( 'h' * N, *xrek )
        wfw.writeframes(data)
    
    wf.close()
    wfw.close()


def calculate_compression_data(wav, total_stream, fs, bits_per_sample = 16):
    # calculating input and output data rates
    input_data_rate = fs * bits_per_sample
    output_data_rate = len(total_stream) / (len(wav) / fs)

    # calculating compression rate
    compression_rate = input_data_rate / output_data_rate
    return input_data_rate, output_data_rate, compression_rate



