import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
import wave
import struct
from analysis_matrix import *
from synthesis_matrix import *
from calc_qmfsubband import *

#N=1024  #number of subbands of the QMF filter bank
N=64

if __name__ == '__main__':

        #import IOMethods as io

        #qmfrt_example()
        
        #global N  #number of subbands
           #global overlap 
        #qmfwin=np.loadtxt('qmf1024_8x.mat');
        #qmfwin=np.hstack((qmfwin,np.flipud(qmfwin)))
        qmfwin=np.loadtxt('qmf.dat');
        plt.plot(qmfwin)
        plt.title('PQMF Prototype Function (Window),'+str(N)+' Subbands')
        plt.show(block=False)
        #plt.show()
        plt.figure()
        w,H=scipy.signal.freqz(qmfwin)
        plt.plot(w,20*np.log10(abs(H)))
        plt.title('Its Magnitude Frequency Response')
        #plt.show(block=False)
        plt.show()
        #Analysis Folding matrix:
        Fa=ha2Fa3d_fast(qmfwin,N)
        #Synthesis Folding matrix: 
        Fs=hs2Fs3d_fast(qmfwin,N)

        #Open sound file to read:
        wf=wave.open('test.wav','rb');
        nchan=wf.getnchannels();
        bytes=wf.getsampwidth();
        rate=wf.getframerate();
        length=wf.getnframes();
        print("Number of channels: ", nchan);
        print("Number of bytes per sample:", bytes);
        print("Sampling rate: ", rate);
        print("Number of samples:", length);

        #open sound file to write the reconstruced sound:
        wfw = wave.open('testrek.wav', 'wb')
        wfw.setnchannels(1)
        wfw.setsampwidth(2)
        wfw.setframerate(rate)

        print("Start QMF:")
        #Process the audio signal block-wise (N samples) from file and into file:
        for m in range(int(length/N)):
           print("Block number: ", m)
           #Analysis:
           data=wf.readframes(N);
           x = (struct.unpack( 'h' * N, data ));
           y=analysisqmf_realtime(x,Fa,N)
           #plt.plot(y)
           #plt.show(block=False)

           #Synthesis:
           xrek=synthesisqmf_realtime(y,Fs,N)
           #write with 2 Bytes per sample:
           #Convert to short ints:
           xrek=np.array(xrek,dtype='int16')
           data=struct.pack( 'h' * N, *xrek )
           wfw.writeframes(data)
        wf.close()           
        wfw.close()