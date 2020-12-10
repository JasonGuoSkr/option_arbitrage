# @Time    : 2020/12/10 13:07
# @Author  : GUO LULU

import numpy as np
import matplotlib.pyplot as plt


def hp(y, lamb=10):
    def D_matrix(N):
        D = np.zeros((N-1,N))
        D[:,1:] = np.eye(N-1)
        D[:,:-1] -= np.eye(N-1)
        """D1
        [[-1.  1.  0. ...  0.  0.  0.]
         [ 0. -1.  1. ...  0.  0.  0.]
         [ 0.  0. -1. ...  0.  0.  0.]
         ...
         [ 0.  0.  0. ...  1.  0.  0.]
         [ 0.  0.  0. ... -1.  1.  0.]
         [ 0.  0.  0. ...  0. -1.  1.]]
        """
        return D
    N = len(ts)
    D1 = D_matrix(N)
    D2 = D_matrix(N-1)
    D = D2 @ D1
    g = np.linalg.inv((np.eye(N)+lamb*D.T@D))@ ts
    return g
