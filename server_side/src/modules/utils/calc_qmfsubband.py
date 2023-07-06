import numpy as np
from src.modules.utils.dct import *



def optimfuncQMF(x,N):
    import numpy as np
    import scipy as sp
    import scipy.signal as sig

    h = np.append(x,np.flipud(x))
    f,H_im = sig.freqz(h)
    H=np.abs(H_im)
    posfreq = np.square(H[0:int(512/N)])
    negfreq = np.flipud(np.square(H[0:int(512/N)]))
    unitycond = np.sum(np.abs(posfreq+negfreq - 2 * (N * N) * np.ones(int(512/N))))/512
    att = np.sum(np.abs(H[int(1.5*512/N):]))/512
    err = unitycond + 100 * att
    return err
                              
def pqmf_analysis_filterbank(x, Fa, N):
    from src.modules.utils.matrix import x2polyphase, polmatmult
    # Pseudo Quadrature Mirror analysis filter bank.
    # Arguments: x: input signal, e.g. audio signal, a 1−dim. array
    # N: number of subbands
    # fb: coefficients for the Quadrature filter bank.
    # returns y, consisting of blocks of subband in in a 2−d array of shape (N,# of blocks)

    # print("Fa.shape=", Fa.shape)

    y = x2polyphase(x, N)
    # print(f'y shape: {y.shape}')
    # print("y[:,:,0]=", y[:, :, 0])

    y = polmatmult(y, Fa)
    y = polmatmult(y, DCToMatrix(N))
    # print(f'y shape: {y.shape}')
    # strip first dimension:
    # y = y[0, :, :]
    return y

def pqmf_analysis_filterbank_fast(x, Fa, N, blockmemory, overlap):
    from src.modules.utils.analysis_matrix import ha2Fa3d_fast
    
    blockmemory[0:(overlap-1),:]=blockmemory[1:(overlap),:]
    #write new block into top of memory stack:
    blockmemory[overlap-1,:]= x
    y=np.zeros((1,N))
    #print "Fa.shape =", Fa.shape
    #Block convolution:
    for m in range(overlap):
        y+=np.dot(np.array([blockmemory[overlap-1-m,:]]), Fa[:,:,m])
    #fast DCT4:
    y=DCT4(y)
    return y

def pqmf_synthesis_filterbank_fast(y,Fs, N, blockmemorysyn, overlap):
    from src.modules.utils.synthesis_matrix import hs2Fs3d_fast

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

def pqmf_synthesis_filterbank(y,Fs, N):
    from src.modules.utils.matrix import polyphase2x, polmatmult
    # Pseudo Quadrature Mirror synthesis filter bank.
    # Arguments: y: 2−d array of blocks of subbands, of shape (N, # of blokcs) #fb: prototype impulse response
    # returns xr, the reconstructed signal, a 1−d array.
    # print(f'y shape: {y.shape}')
    # print(f'N: {N}')

    xrekp=polmatmult(y,DCToMatrix(N))
    xrekp=polmatmult(xrekp,Fs)
    xrek=polyphase2x(xrekp)
    return xrek

