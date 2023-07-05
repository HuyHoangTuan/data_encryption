import numpy as np
from mult_matrix import *
from dct import *

def ha2Pa3d(ha,N):
        #usage: Pa=ha2Pa3d(ha,N);
        #produces the analysis polyphase matrix Pa
        #in 3D matrix representation
        #from a basband filter ha with
        #a cosine modulation
        #N: Blocklength
        #Gerald Schuller
        #shl@idmt.fhg.de
        #Dec-2-15

        L=len(ha);

        blocks=int(np.ceil(L/N));
        #print(blocks)

        Pa=np.zeros((N,N,blocks));

        for k in range(N): #subband
          for m in range(blocks):  #m: block number 
            for nphase in range(N): #nphase: Phase 
              n=m*N+nphase;
              #indexing like impulse response, phase index is reversed (N-np):
              Pa[N-1-nphase,k,m]=ha[n]*np.sqrt(2.0/N)*np.cos(np.pi/N*(k+0.5)*(blocks*N-1-n-N/2.0+0.5)); 

        return Pa


def ha2Fa3d(ha,N):
        #usage: Fa=ha2Fa3d(ha,N);
        #produces the analysis polyphase folding matrix Fa with all polyphase components
        #in 3D matrix representation
        #from a basband filter ha with
        #a cosine modulation
        #N: Blocklength
        #Gerald Schuller
        #shl@idmt.fhg.de
        #Dec-2-15
        print("ha2Pa3d:")
        Pa=ha2Pa3d(ha,N);
        print("polmatmult DCT:")
        Fa=polmatmult(Pa,DCToMatrix(N))
        #round zeroth polyphase component to 7 decimals after point:
        Fa=np.around(Fa,8)

        return Fa

def ha2Fa3d_fast(qmfwin,N):
        #usage: Fa=ha2Fa3d_fast(ha,N);
        #produces the analysis polyphase folding matrix Fa with all polyphase components
        #in 3D matrix representation
        #from a basband filter ha with
        #a cosine modulation
        #N: Blocklength
        #using a fast implementation (important for large N)
        #See my book chapter about "Filter Banks", cosine modulated filter banks.
        #Gerald Schuller
        #shl@idmt.fhg.de
        #Jan-23-16
        overlap=int(len(qmfwin)/N)
        print("overlap=", overlap)
        Fa=np.zeros((N,N,overlap))
        for m in range(int(overlap/2)):
           Fa[:,:,2*m]+=np.fliplr(np.diag(np.flipud(-qmfwin[m*2*N:(m*2*N+int(N/2))]*((-1)**m)),k=int(-N/2)))
           Fa[:,:,2*m]+=(np.diag(np.flipud(qmfwin[m*2*N+int(N/2):(m*2*N+N)]*((-1)**m)),k=int(N/2)))
           Fa[:,:,2*m+1]+=(np.diag(np.flipud(qmfwin[m*2*N+N:(m*2*N+int(1.5*N))]*((-1)**m)),k=-int(N/2)))
           Fa[:,:,2*m+1]+=np.fliplr(np.diag(np.flipud(qmfwin[m*2*N+int(1.5*N):(m*2*N+2*N)]*((-1)**m)),k=int(N/2)))
           #print -qmfwin[m*2*N:(m*2*N+N/2)]*((-1)**m)
        return Fa