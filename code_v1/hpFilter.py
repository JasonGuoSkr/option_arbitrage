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


if __name__ == '__main__':
    N = 100
    t = np.linspace(1,10,N)
    ts = np.sin(t) + np.cos(20*t) + np.random.randn(N)*0.1

    plt.figure(figsize=(10,12))
    for i,l in enumerate([0.1,1,10,100,1000, 10000]):
        plt.subplot(3,2,i+1)
        g = hp(ts,l)
        plt.plot(ts, label='original')
        plt.plot(g, label='filtered')
        plt.legend()
        plt.title('$\lambda$='+str(l))
    plt.show()
