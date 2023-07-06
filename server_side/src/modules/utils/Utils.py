import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import io
import os
from src.modules.utils.Common import *
from src.modules.utils.Parameters import *
import src.modules.utils.PrototypeFilter as PrototypeFilter
import src.modules.utils.SubbanFiltering as SubbanFiltering
import src.modules.utils.Psychoacoustic as Psychoacoustic
import src.modules.utils.Quantization as Quantization

def plotSubbands(subbands, M=32):
    # Create a figure and axes
    fig, ax = plt.subplots()
    fig.set_size_inches(18.5, 10.5, forward=True)
    subbands_freq = np.fft.fft(subbands)

    # Calculate the frequency values for the x-axis
    sample_rate = 44100  # Assuming a sample rate of 1000 Hz
    frequency = np.fft.fftfreq(subbands.shape[1], d=1/sample_rate)

    color = cm.rainbow(np.linspace(0, 1, M))
    # Plot the magnitude spectrum for each subband
    for i in range(subbands_freq.shape[0]):
        magnitude_spectrum = np.abs(subbands_freq[i])
        ax.plot(frequency, magnitude_spectrum, label=f"Subband {i+1}", c = color[i])

    # Add labels and a legend
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.legend(bbox_to_anchor=(1, 1))

    # output_filename = 'my_plot.png'
    # plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    
    # Show the plot
    # plt.show()
    
    # Encode the plot as a byte array
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='PNG')
    image_stream.seek(0)
    # image_bytes = image_stream.read()
    plt.close('all')
    return image_stream

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



def compress_mp3_with_custom_bit_rate(wav_file, bit_rate):
    input_buffer = WavRead(wav_file)
    params = EncoderParameters(input_buffer.fs, input_buffer.nch, bit_rate)

    baseband_filter = PrototypeFilter.process().astype('float32')

    subband_samples = np.zeros((params.nch, N_SUBBANDS, FRAMES_PER_BLOCK), dtype='float32')

    object_mp3 = {
        'params': [],
        'subband_bit_allocation': [],
        'scfindices': [],
        'subband_samples_quantized': []
    }

    object_mp3_len = 0
    print(f'Compressing file: {params.nch} -- {input_buffer.nsamples}')
    while input_buffer.nprocessed_samples < input_buffer.nsamples:
        for frm in range(FRAMES_PER_BLOCK):
            samples_read = input_buffer.read_samples(SHIFT_SIZE)

            if samples_read < SHIFT_SIZE:
                for ch in range(params.nch):
                    input_buffer.audio[ch].insert(np.zeros(SHIFT_SIZE - samples_read))

            # Filtering 
            for ch in range(params.nch):
                subband_samples[ch,:,frm] = SubbanFiltering.process(input_buffer.audio[ch].reversed(), baseband_filter)

        # print('subband_samples', subband_samples.shape)
        scfindices = np.zeros((params.nch, N_SUBBANDS), dtype='uint8')
        subband_bit_allocation = np.zeros((params.nch, N_SUBBANDS), dtype='uint8') 
        smr = np.zeros((params.nch, N_SUBBANDS), dtype='float32')
        
        for ch in range(params.nch):
            scfindices[ch,:] = get_scalefactors(subband_samples[ch,:,:], params.table.scalefactor)
            subband_bit_allocation[ch,:] = Psychoacoustic.model1(input_buffer.audio[ch].ordered(), params,scfindices)

        # Quantization
        subband_samples_quantized = np.zeros(subband_samples.shape, dtype='uint32')
        for ch in range(params.nch):
            for sb in range(N_SUBBANDS):
                QCa = params.table.qca[subband_bit_allocation[ch,sb]-2]
                QCb = params.table.qcb[subband_bit_allocation[ch,sb]-2]
                scf = params.table.scalefactor[scfindices[ch,sb]]
                ba = subband_bit_allocation[ch,sb]
                for ind in range(FRAMES_PER_BLOCK):
                    subband_samples_quantized[ch,sb,ind] = Quantization.process(subband_samples[ch,sb,ind], scf, ba, QCa, QCb)


        object_mp3['params'].append(params)
        object_mp3['subband_bit_allocation'].append(subband_bit_allocation)
        object_mp3['scfindices'].append(scfindices)
        object_mp3['subband_samples_quantized'].append(subband_samples_quantized)
        object_mp3_len += 1

        
    # print("Compression Rate: (by bitrate): ", (input_buffer.nbits * input_buffer.fs / 1000) / bitrate)
    
    object_mp3['len'] = object_mp3_len
    object_mp3['compression_rate_by_bit_rate'] = (input_buffer.nbits * input_buffer.fs / 1000) / bit_rate
    return object_mp3

    # return params, subband_bit_allocation, scfindices, subband_samples_quantized

def process_plot_subbands(wav_file, bit_rate):
    input_buffer = WavRead(wav_file)
    params = EncoderParameters(input_buffer.fs, input_buffer.nch, bit_rate)

    baseband_filter = PrototypeFilter.process().astype('float32')
    
    subband_samples = np.zeros((params.nch, N_SUBBANDS, FRAMES_PER_BLOCK), dtype='float32')

    total_subbands = np.empty((1, N_SUBBANDS ,0))

    print(f'Ploting file: {params.nch} -- {input_buffer.nsamples}')
    while input_buffer.nprocessed_samples < input_buffer.nsamples:
        for frm in range(FRAMES_PER_BLOCK):
            samples_read = input_buffer.read_samples(SHIFT_SIZE)

            if samples_read < SHIFT_SIZE:
                for ch in range(params.nch):
                    input_buffer.audio[ch].insert(np.zeros(SHIFT_SIZE - samples_read))

            # Filtering 
            for ch in range(params.nch):
                subband_samples[ch,:,frm] = SubbanFiltering.process(input_buffer.audio[ch].reversed(), baseband_filter)

        total_subbands = np.concatenate((total_subbands, subband_samples), axis=2)

    total_subbands = np.reshape(total_subbands, (N_SUBBANDS, -1))
    return plotSubbands(total_subbands, N_SUBBANDS)

def save_mp3(outpt_file, params, subband_bit_allocation, scfindices, subband_samples_quantized):
    bitstream_formatting(outpt_file, params, subband_bit_allocation, scfindices, subband_samples_quantized)

def calculate_compression_data(wav, total_stream, fs, bits_per_sample = 16):
    # calculating input and output data rates
    input_data_rate = fs * bits_per_sample
    output_data_rate = len(total_stream) / (len(wav) / fs)

    # calculating compression rate
    compression_rate = input_data_rate / output_data_rate
    return input_data_rate, output_data_rate, compression_rate



