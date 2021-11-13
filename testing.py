import cv2
import numpy as np
import time
import sys
import os
from numpy.linalg import svd
from SVD_bener import svd_nguli


def compressImage(imagePart, scale):
    U, S, VT = svd_nguli(imagePart)
    #sourceFile = open('demo.txt', 'w')
    # np.set_printoptions(threshold=sys.maxsize)
    #print(S, file=sourceFile)
    #print("==============================================================", file=sourceFile)
    # sourceFile.close()
    # exit()
    S = np.diag(S)
    X = U[:, :scale] @ S[:scale, :scale] @ VT[:scale, :]
    X = cv2.normalize(X, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    return X

filename = input()
image = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
factor = float(input())
panjang = image.shape[0]
tinggi = image.shape[1]
print("bytes",image.nbytes)
if (panjang > tinggi):
    scale = int(factor*tinggi)
else:
    scale = int(factor*panjang)
start_time = time.time()
if (image.shape[2] == 1):
    resImage = compressImage(image, scale)
elif (image.shape[2] == 3):
    (B, G, R) = cv2.split(image)
    B = B.astype(float)
    G = G.astype(float)
    R = R.astype(float)
    newB = compressImage(B, scale)
    newG = compressImage(G, scale)
    newR = compressImage(R, scale)
    resImage = cv2.merge([newB, newG, newR])
else:  # GBRA image
    (B, G, R, A) = cv2.split(image)
    B = B.astype(float)
    G = G.astype(float)
    R = R.astype(float)
    A = A.astype(float)
    newB = compressImage(B, scale)
    newG = compressImage(G, scale)
    newR = compressImage(R, scale)
    newA = compressImage(A, scale)
    resImage = cv2.merge([newB, newG, newR, newA])
    filename = "compressed.png"
print("--- %s seconds ---" % (time.time() - start_time))
cv2.imshow("ImageCompressed", resImage)
print("bytes",image.nbytes)
head, tail = os.path.split(filename)
split_name = os.path.splitext(tail)
newname = split_name[-2] + "_compressed" + split_name[-1]
resImage.save(newname)
