import sys
import os.path
import numpy as np
import psychoacoustic as psycho
from common import *
from parameters import *

import matplotlib.pyplot as plt 
from matplotlib.pyplot import cm
import io
import os

import prototype_filter
import subband_filtering
import quantization

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
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    image_bytes = image_stream.read()
    plt.close()
    return image_bytes

def main(inwavfile, outmp3file, bitrate):
  """Encoder main function."""

  #inwavfile  = "../samples/sinestereo.wav"
  #outmp3file = "../samples/sinestereo.mp3"
  #bitrate = 320
  
  
  # Read WAVE file and set MPEG encoder parameters.
  input_buffer = WavRead(inwavfile)
  params = EncoderParameters(input_buffer.fs, input_buffer.nch, bitrate)
  total_subbands = np.empty((input_buffer.nch,32,0))

  
  # Subband filter calculation from baseband prototype.
  # Very detailed analysis of MP3 subband filtering available at
  # http://cnx.org/content/m32148/latest/?collection=col11121/latest

  # Read baseband filter samples
  """
  Prototype-filter
  """
  baseband_filter = prototype_filter.prototype_filter().astype('float32')

  subband_samples = np.zeros((params.nch, N_SUBBANDS, FRAMES_PER_BLOCK), dtype='float32') 

  # Main loop, executing until all samples have been processed.
  while input_buffer.nprocessed_samples < input_buffer.nsamples:

    # In each block 12 frames are processed, which equals 12x32=384 new samples per block.
    for frm in range(FRAMES_PER_BLOCK):
      samples_read = input_buffer.read_samples(SHIFT_SIZE)

      # If all samples have been read, perform zero padding.
      if samples_read < SHIFT_SIZE:
        for ch in range(params.nch):
          input_buffer.audio[ch].insert(np.zeros(SHIFT_SIZE - samples_read))

      # Filtering = dot product with reversed buffer.
      """
       Subband filtering
      """
      for ch in range(params.nch):
        subband_samples[ch,:,frm] = subband_filtering.subband_filtering(input_buffer.audio[ch].reversed(), baseband_filter)

    total_subbands = np.concatenate((total_subbands, subband_samples), axis=2)
      # print(total_subbands.shape)
    
    # Declaring arrays for keeping table indices of calculated scalefactors and bits allocated in subbands.
    # Number of bits allocated in subband is either 0 or in range [2,15].
    scfindices = np.zeros((params.nch, N_SUBBANDS), dtype='uint8')
    subband_bit_allocation = np.zeros((params.nch, N_SUBBANDS), dtype='uint8') 
    smr = np.zeros((params.nch, N_SUBBANDS), dtype='float32')

    
    # Finding scale factors, psychoacoustic model and bit allocation calculation for subbands. Although 
    # scaling is done later, its result is necessary for the psychoacoustic model and calculation of 
    # sound pressure levels.
    for ch in range(params.nch):
      scfindices[ch,:] = get_scalefactors(subband_samples[ch,:,:], params.table.scalefactor)
      subband_bit_allocation[ch,:] = psycho.model1(input_buffer.audio[ch].ordered(), params,scfindices)

    """
    Quantization
    """
    subband_samples_quantized = np.zeros(subband_samples.shape, dtype='uint32')
    for ch in range(params.nch):
      for sb in range(N_SUBBANDS):
        QCa = params.table.qca[subband_bit_allocation[ch,sb]-2]
        QCb = params.table.qcb[subband_bit_allocation[ch,sb]-2]
        scf = params.table.scalefactor[scfindices[ch,sb]]
        ba = subband_bit_allocation[ch,sb]
        for ind in range(FRAMES_PER_BLOCK):
          subband_samples_quantized[ch,sb,ind] = quantization.quantization(subband_samples[ch,sb,ind], scf, ba, QCa, QCb)


    # Forming output bitsream and appending it to the output file.
    bitstream_formatting(outmp3file,
                         params,
                         subband_bit_allocation,
                         scfindices,
                         subband_samples_quantized)
  
  for i in range(total_subbands.shape[0]):
    plotSubbands(total_subbands[i])
  print("Compression Rate: (by bitrate): ", (input_buffer.nbits * input_buffer.fs / 1000) / bitrate)
  print("Compression Rate: (by filesize): ", os.stat(inwavfile).st_size / os.stat(outmp3file).st_size)

if __name__ == "__main__":
  if len(sys.argv) < 3:
    sys.exit('Please provide input WAVE file and desired bitrate.')
  inwavfile = sys.argv[1]
  if len(sys.argv) == 4:
    outmp3file = sys.argv[2]
    bitrate    = int(sys.argv[3])
  else:
    outmp3file = inwavfile[:-3] + 'mp3'
    bitrate    = int(sys.argv[2])

  if os.path.exists(outmp3file):
    sys.exit('Output file already exists.')

  main(inwavfile,outmp3file,bitrate)
