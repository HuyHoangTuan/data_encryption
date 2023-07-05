import numpy as np
from dct import *

#N=1024  #number of subbands of the QMF filter bank
N=64
#internal memory for the input blocks, for 8 times overlap:
overlap=8;
blockmemory=np.zeros((overlap,N))
blockmemorysyn=np.zeros((overlap,N))

def analysisqmf_realtime(xrt,Fa,N):
        #computes the QMF subband samples for each real time input block xrt. 
        #Conducts an implicit polynomial multiplication with folding matrix Fa of 
        #the polyphase matrix of the QMF filter bank, using
        #internal memory of the past input blocks.

        #from scipy import sparse
        global blockmemory
        global overlap
        #push down old blocks:
        blockmemory[0:(overlap-1),:]=blockmemory[1:(overlap),:]
        #write new block into top of memory stack:
        blockmemory[overlap-1,:]=xrt;
        y=np.zeros((1,N));
        #print "Fa.shape =", Fa.shape
        #Block convolution:
        for m in range(overlap):
           y+=np.dot(np.array([blockmemory[overlap-1-m,:]]), Fa[:,:,m])
           #y+= (sparse.csr_matrix(blockmemory[overlap-1-m,:]).dot(sparse.csr_matrix(Fa[:,:,m]))).todense()
        #fast DCT4:
        y=DCT4(y)
        return y

def synthesisqmf_realtime(y,Fs,N):
        #computes the inverse QMF for each subband block y, 
        #conducts an implicit polynomial multiplication with synthesis folding matrix Fs 
        #of the synthesis polyphase matrix of the QMF filter bank, using
        #internal memory for future output blocks.

        #from scipy import sparse
        global blockmemorysyn
        global overlap
        #print "overlap= ", overlap
        #push down old blocks:
        blockmemorysyn[0:(overlap-1),:]=blockmemorysyn[1:(overlap),:]
        blockmemorysyn[overlap-1,:]=np.zeros((1,N)) #avoid leaving previous values in top of memory.
        #print "memory content synthesis: ", np.sum(np.abs(blockmemorysyn))
        #print "Fs.shape =", Fs.shape
        #print "y.shape= ", y.shape
        #Overlap-add after fast (inverse) DCT4, block convolution:
        for m in range(overlap):
           blockmemorysyn[m,:]+=np.dot(DCT4(y), Fs[:,:,m])
           #y+= (sparse.csr_matrix(blockmemory[overlap-1-m,:]).dot(sparse.csr_matrix(Fa[:,:,m]))).todense()
        xrek=blockmemorysyn[0,:]
        
        
        return xrek