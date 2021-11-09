from os import truncate
import numpy as np
from numpy.lib.twodim_base import diag


def simultaneous_power_iteration(A, k):
    n, m = A.shape
    Q = np.random.rand(n, k)
    Q, _ = np.linalg.qr(Q)
    Q_prev = Q

    for i in range(250):
        Z = A.dot(Q)
        Q, R = np.linalg.qr(Z)

        # can use other stopping criteria as well
        err = ((Q - Q_prev) ** 2).sum()
        # if i % 10 == 0:
        # print(i, err)

        Q_prev = Q
        if err < 1e-6:
            break

    return np.diag(R), Q


def svd_nguli(A: np):
    AT = A.transpose()

    # singular kiri
    AxAT: np = A@AT
    singular_kiri = simultaneous_power_iteration(AxAT, len(AxAT[0]))
    U: np = singular_kiri[1]

    # Sigma
    S = singular_kiri[0]
    S.setflags(write=1)
    found = False
    t = 0
    for i in range(len(S)):
        # if(S[i] < 1e-3):
        # if(not(found)):
        #t = i
        #found = True
        if (S[i] == 0):
            S[i] = 1e-12
        if(S[i] < 0):
            S[i] *= -1
    S = np.sqrt(S)
    Sigma = np.diag(S)

    Uinv = np.linalg.inv(U)
    Sinv = np.linalg.inv(Sigma)
    VT = Sinv@Uinv@A
    # if (found):
    #VT = VT[:t]
    #S = S[:t]
    return U, S, VT
