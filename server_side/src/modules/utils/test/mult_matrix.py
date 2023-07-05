

import numpy as np
from scipy import sparse

def polmatmult(A,B):
        #function C=polmatmult(A,B)
        #multiplies 2 polynomial matrices A and B, where each matrix entry is a polynomial, e.g. in z^-1.
        #Those polynomial entries are in the 3rd dimension 
        #The third dimension can also be interpreted as containing the (2D) coefficient matrices for each 
        #exponent of z^-1. 
        #Result is C=A*B;

        [NAx,NAy,NAz]=A.shape;
        [NBx,NBy,NBz]=B.shape;

        #Degree +1 of resulting polynomial, with NAz-1 and NBz-1 beeing the degree of the input  polynomials:
        Deg=NAz+NBz-1;

        C=np.zeros((NAx,NBy,Deg));

        for n in range(Deg):
          for m in range(n+1):
            if ((n-m)<NAz and m<NBz):
              C[:,:,n]=C[:,:,n]+ A[:,:,(n-m)].dot(B[:,:,m])
              #sparse version:
              #C[:,:,n]=C[:,:,n]+ (sparse.csr_matrix(A[:,:,(n-m)]).dot(sparse.csr_matrix(B[:,:,m]))).todense()
        return C
