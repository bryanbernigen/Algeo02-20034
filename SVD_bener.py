import numpy as np
from numpy.lib.twodim_base import diag


def eig_val_and_vect(Matrix, jumlah):
    baris, kolom = Matrix.shape
    Q = np.random.rand(baris, jumlah)
    Q, _ = np.linalg.qr(Q)
    Prev_Q = Q

    for i in range(250):
        A = Matrix.dot(Q)
        Q, R = np.linalg.qr(A)
        error = ((Q-Prev_Q)**2).sum()
        Prev_Q = Q
        if error < 1e-6:
            break

    return np.diag(R), Q


def svd_nguli(A: np):
    AT = A.transpose()

    # singular kiri
    AxAT: np = A@AT
    singular_kiri = eig_val_and_vect(AxAT, len(AxAT[0]))
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
