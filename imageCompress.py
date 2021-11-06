import cv2
import numpy as np

def compressImage(imagePart, scale):
    U,S,VT = np.linalg.svd(imagePart,full_matrices = False)
    S = np.diag(S)
    X = U[:,:scale] @ S[:scale,:scale] @ VT[:scale,:]
    X = cv2.normalize(X, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    return X

image = cv2.imread("imgX.jpg", cv2.IMREAD_UNCHANGED)
scale = 10
if (image.shape[2] == 1) :
    resImage = compressImage(image,scale)
elif (image.shape[2] == 3):
    (B,G,R) = cv2.split(image)
    newB = compressImage(B,scale)
    newG = compressImage(G,scale)
    newR = compressImage(R,scale)
    resImage = cv2.merge([newB,newG,newR])
else: #GBRA image
    (B,G,R,A) = cv2.split(image)
    newB = compressImage(B,scale)
    newG = compressImage(G,scale)
    newR = compressImage(R,scale)
    newA = compressImage(A,scale)
    resImage = cv2.merge([newB,newG,newR, newA])
cv2.imshow("ImageCompressed", resImage)
cv2.waitKey(0)
