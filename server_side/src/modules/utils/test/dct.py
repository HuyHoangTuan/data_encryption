import numpy as np
import scipy.fftpack as spfft

N = 64

def DCToMatrix(N):
        #produces an odd DCT matrix with size NxN
        #Gerald Schuller, Dec. 2015

        y=np.zeros((N,N,1));

        for n in range(N):
           for k in range(N):
              y[n,k,0]=np.sqrt(2.0/N)*np.cos(np.pi/N*(k+0.5)*(n+0.5));
              #y(n,k)=cos(pi/N*(k-0.5)*(n-1));
        return y   

#The DCT4 transform:
def DCT4(samples):
   #use a DCT3 to implement a DCT4:
   samplesup=np.zeros(2*N)
   #upsample signal:
   samplesup[1::2]=samples
   y=spfft.dct(samplesup,type=3,norm='ortho')*np.sqrt(2)#/2
   return y[0:N]