import numpy as np
from scipy import sparse


def polmatmult(A, B):
    # function C=polmatmult(A,B)
    # multiplies 2 polynomial matrices A and B, where each matrix entry is a polynomial, e.g. in z^-1.
    # Those polynomial entries are in the 3rd dimension 
    # The third dimension can also be interpreted as containing the (2D) coefficient matrices for each 
    # exponent of z^-1. 
    # Result is C=A*B;

    [NAx, NAy, NAz] = np.shape(A)
    [NBx, NBy, NBz] = np.shape(B)
    #Degree +1 of resulting polynomial, with NAz−1 and NBz−1 being the degree of the... 
    Deg = NAz + NBz -1
    C = np.zeros((NAx,NBy,Deg))
    #Convolution of matrices:
    for n in range(0,(Deg)):
        for m in range(0,n+1):
            if ((n-m)<NAz and m<NBz):
                C[:,:,n] = C[:,:,n]+ np.dot(A[:,:,(n-m)],B[:,:,m])
    return C


def polyphase2x(xp):
    """Converts polyphase input signal xp (a row vector) into a contiguos row vector For block length N, for 3D polyphase representation (exponents of z in the third matrix/tensor dimension)"""
    x=np.reshape(xp,(1,1,-1), order='F') #order=F: first index changes fastest 
    x=x[0,0,:]
    return x


def x2polyphase(x, N):
    """Converts input signal x (a 1D array) into a polyphase row vector
    xp for blocks of length N, with shape: (1,N,#of blocks)"""
    import numpy as np
    #Convert stream x into a 2d array where each row is a block:
    #xp.shape : (y,x, #num blocks):
    x=x[:int(len(x)/N)*N] #limit signal to integer multiples of N 
    xp=np.reshape(x,(N,-1),order='F')
    xp=np.expand_dims(xp,axis=0)
    return xp
