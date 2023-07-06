
import numpy as np
from src.modules.utils.dct import *
from src.modules.utils.matrix import *

def hs2Ps3d(hs,N):
        #usage: Ps=hs2Ps3d(hs,N);
        #produces the synthesis polyphase matrix Ps
        #in 3D matrix representation
        #from a basband filter hs with
        #a cosine modulation
        #N: Blocklength
        #Gerald Schuller
        #shl@idmt.fhg.de
        #Dec-2-15

        L=len(hs);

        blocks=int(np.ceil(L/N));
        #print(blocks)

        Ps=np.zeros((N,N,blocks));

        for k in range(N): #subband
          for m in range(blocks):  #m: block number 
            for nphase in range(N): #nphase: Phase 
              n=m*N+nphase;
              #synthesis:
              Ps[k,nphase,m]=hs[n]*np.sqrt(2.0/N)*np.cos(np.pi/N*(k+0.5)*(n-N/2.0+0.5)); 

        return Ps
    
def hs2Fs3d_fast(qmfwin, N):
        #usage: Fs=hs2Fs3d_fast(hs,N);
        #produces the synthesis polyphase folding matrix Fs with all polyphase components
        #in 3D matrix representation
        #from a basband filter ha with
        #a cosine modulation
        #N: Blocklength
        #Fast implementation
        #Gerald Schuller
        #shl@idmt.fhg.de
        #Jan-23-15

        #Fa=ha2Fa3d_fast(hs,N)
        #print "Fa.shape in hs2Fs : ", Fa.shape
        #Transpose first two dimensions to obtain synthesis folding matrix:
        #Fs=np.transpose(Fa, (1, 0, 2))
        overlap=int(len(qmfwin)/N)
        # print("overlap=", overlap)
        Fs=np.zeros((N,N,overlap))
        for m in range(int(overlap/2)):
           Fs[:,:,2*m]+=np.fliplr(np.diag(np.flipud(qmfwin[m*2*N:(m*2*N+int(N/2))]*((-1)**m)),k=int(N/2)))
           Fs[:,:,2*m]+=(np.diag((qmfwin[m*2*N+int(N/2):(m*2*N+N)]*((-1)**m)),k=int(N/2)))
           Fs[:,:,2*m+1]+=(np.diag((qmfwin[m*2*N+N:(m*2*N+int(1.5*N))]*((-1)**m)),k=int(-N/2)))
           Fs[:,:,2*m+1]+=np.fliplr(np.diag(np.flipud(-qmfwin[m*2*N+int(1.5*N):(m*2*N+2*N)]*((-1)**m)),k=int(-N/2)))
        #print "Fs.shape in hs2Fs : ", Fs.shape
        #avoid sign change after reconstruction:
        return -Fs
    

def hs2Fs3d(hs,N):
        #usage: Fs=hs2Fs3d(hs,N);
        #produces the synthesis polyphase folding matrix Fs with all polyphase components
        #in 3D matrix representation
        #from a basband filter ha with
        #a cosine modulation
        #N: Blocklength
        #Gerald Schuller
        #shl@idmt.fhg.de
        #Dec-2-15

        Ps=hs2Ps3d(hs,N);
        Fs=polmatmult(DCToMatrix(N),Ps)
        #round zeroth polyphase component to 7 decimals after point:
        Fs=np.around(Fs,8)

        return Fs