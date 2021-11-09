import numpy as np
from numpy.lib.twodim_base import diag


def simultaneous_power_iteration(A, k):
    n, m = A.shape
    Q = np.random.rand(n, k)
    Q, _ = np.linalg.qr(Q)
    Q_prev = Q

    for i in range(500):
        Z = A.dot(Q)
        Q, R = np.linalg.qr(Z)

        # can use other stopping criteria as well
        err = ((Q - Q_prev) ** 2).sum()
        # if i % 10 == 0:
        # print(i, err)

        Q_prev = Q
        if err < 1e-9:
            break

    return np.diag(R), Q


def svd_nguli(A: np):
    AT = A.transpose()

    # singular kiri
    AxAT: np = A@AT
    singular_kiri = simultaneous_power_iteration(AxAT, len(AxAT[0]))
    UT: np = singular_kiri[1]
    U = UT.transpose()

    # Sigma
    sourceFile = open('demo.txt', 'w')
    S = singular_kiri[0]
    print(S, file=sourceFile)
    sourceFile.close()
    S.setflags(write=1)
    for i in range(len(S)):
        if(S[i] < 0):
            S[i] *= -1
    S = np.sqrt(S)
    Sigma = np.diag(S)

    # singular kanan
    Uinv = np.linalg.inv(U)
    Sinv = np.linalg.inv(Sigma)
    VT = Sinv@Uinv@A

    return U, Sigma, VT
