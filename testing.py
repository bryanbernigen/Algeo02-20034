import cv2
import numpy as np
import time
from SVD_bener import svd_nguli


def compressImage(imagePart, scale):
    U, S, VT = svd_nguli(imagePart)
    X = U[:, :scale] @ S[:scale, :scale] @ VT[:scale, :]
    X = cv2.normalize(X, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    return X


image = cv2.imread("mona.jpg", cv2.IMREAD_UNCHANGED)
scale = 200
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
print("--- %s seconds ---" % (time.time() - start_time))
cv2.imshow("ImageCompressed", resImage)
cv2.waitKey(0)
