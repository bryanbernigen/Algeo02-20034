from math import pi, sqrt
from re import M
from mpmath.functions.functions import sign
import numpy as np
import sympy as sp
from sympy.core import symbol
from sympy.logic.boolalg import to_anf
from sympy.matrices.dense import Matrix, diag, eye
from sympy.matrices.expressions.special import Identity
from sympy.simplify.fu import L
from sympy.solvers.diophantine.diophantine import length
from sympy.tensor.functions import shape
from sympy import I


def solusi_spl(m: sp.Matrix):
    length_pivot: sp.Matrix
    m_reduced = m.rref()
    m_reduced_only = np.array(m_reduced[0])
    length = m_reduced[0].shape[1]
    length_pivot = len(m_reduced[1])
    pivot = m_reduced[1]
    hasil = np.ones((length))
    for i in range(length_pivot):
        for j in range(length-pivot[i]):
            hasil[pivot[i]] -= m_reduced_only[i][j+pivot[i]]
    return hasil


def SVD_function(m: np.matrix):

    # define keseluruhan
    x, y, z = sp.symbols('x,y,z')

    def pliss_masuk_lamda(i, j):
        if i == j:
            return x
        else:
            return 0

    # define singular kiri
    np_AxAT: np.matrix
    sp_AIminAxAT_kiri: sp.Matrix

    # define singular kanan
    sp_AIminAxAT_kiri: sp.Matrix
    sp_AIminATxA_kanan: sp.Matrix

    # ==============================Singular Kiri=====================================
    # Bikin matrix A, AT, dan AxAT
    A = m
    AT = A.transpose()
    np_AxAT = np.matmul(A, AT)
    sp_AxAT = sp.Matrix(np_AxAT)
    # bikin matrix lamdaxIdentitas dan matrix AxA^T - matrix lamdaxIdentitas
    n = sp_AxAT.shape[1]
    sp_AI_kiri = Matrix(n, n, pliss_masuk_lamda)
    sp_AxATminAI = sp_AxAT - sp_AI_kiri
    # Cari nilai-nilai eigen
    print(sp_AxATminAI)
    nilai_eigen_kiri = sp.solvers.solve(sp_AxATminAI.det())
    jumlah_nilai_eigen_kiri = np.array(nilai_eigen_kiri).size
    nilai_sigma = []
    for i in range(jumlah_nilai_eigen_kiri):
        nilai_sigma.append(sqrt(nilai_eigen_kiri[jumlah_nilai_eigen_kiri-1-i]))
    # bikin vektor eigen
    UT = []
    for i in range(jumlah_nilai_eigen_kiri):
        # substitusi lamda ke matrixnya + cari solusinya buat jadi vektor eigen
        sp_AIminAxAT_kiri = sp_AI_kiri.subs(
            x, nilai_eigen_kiri[jumlah_nilai_eigen_kiri-1-i])-np_AxAT
        vektor_eigen_kiri = solusi_spl(sp_AIminAxAT_kiri)
        baris_UT = []
        pembagi = 0
        for j in range(jumlah_nilai_eigen_kiri):
            pembagi += vektor_eigen_kiri[j]*vektor_eigen_kiri[j]
        pembagi = sqrt(pembagi)
        for j in range(jumlah_nilai_eigen_kiri):
            baris_UT.append(vektor_eigen_kiri[j]/pembagi)
        UT.append(baris_UT)
    UT = np.array(UT)
    U = UT.transpose()

    # =============================Singular Kanan=====================================
    # Bikin matrix A, AT, dan ATxA
    A = m
    AT = A.transpose()
    np_ATxA = np.matmul(AT, A)
    sp_ATxA = sp.Matrix(np_ATxA)
    # bikin matrix lamdaxIdentitas dan matrix AxA^T - matrix lamdaxIdentitas
    n_kanan = sp_ATxA.shape[1]
    sp_AI_kanan = Matrix(n_kanan, n_kanan, pliss_masuk_lamda)
    sp_ATxAminAI = sp_ATxA - sp_AI_kanan
    # Cari nilai-nilai eigen
    nilai_eigen_kanan = sp.solvers.solve(sp_ATxAminAI.det())
    jumlah_nilai_eigen_kanan = np.array(nilai_eigen_kanan).size
    # bikin vektor eigen
    VT = []
    for i in range(jumlah_nilai_eigen_kanan):
        # substitusi lamda ke matrixnya + cari solusinya buat jadi vektor eigen
        sp_AIminATxA_kanan = sp_AI_kanan.subs(
            x, nilai_eigen_kanan[jumlah_nilai_eigen_kanan-1-i])-np_ATxA
        vektor_eigen_kanan = solusi_spl(sp_AIminATxA_kanan)
        baris_VT = []
        pembagi = 0
        for j in range(jumlah_nilai_eigen_kanan):
            pembagi += vektor_eigen_kanan[j]*vektor_eigen_kanan[j]
        pembagi = sqrt(pembagi)
        for j in range(jumlah_nilai_eigen_kanan):
            baris_VT.append(vektor_eigen_kanan[j]/pembagi)
        VT.append(baris_VT)
    VT = np.array(VT)

    # =============================Nilai-Nilai Singular===============================
    Sigma = [[0 for i in range(n_kanan)] for j in range(n)]
    for i in range(n):
        Sigma[i][i] = nilai_sigma[i]
    Sigma = np.array(Sigma)
    # =================================Hasil==========================================
    print(U @ Sigma @ VT)
    return
'''
m=np.array([[3,1,1],[-1,3,1]])
SVD_function(m)'''

'''m = np.array([[89, 75, 22, 102], [75, 116, 27, 120],
             [22, 27, 33, 62], [102, 120, 62, 200]])'''


