import numpy as np
import math
import random

def getUCB(theta,x,beta,V):
    x_Vnorm = np.dot(np.dot(x,np.linalg.inv(V)),np.transpose(x)) ** 1/2
    UCB = min(np.dot(np.transpose(theta),np.transpose(x)) + beta * x_Vnorm, 1)
    return UCB
    
def update_stat(V,X,hist_X,hist_Y,W,lamb,delta,gama=1):
    newV = V
    numx = X.shape[0]
    for i in range(0,numx):
        newV += np.dot(np.transpose(X[i,:]),X[i,:]) * (gama ** 2)
        X[i,:] = X[i,:] * gama
    newX = np.vstack((hist_X,X))
    numw = W.shape[0]
    for i in range(0,numw):
        W[i,:] = W[i,:] * gama
    newY = np.vstack((hist_Y,W))
    ishape = X.shape[1]
    tmpI = np.identity(ishape) * lamb
    theta = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(X),X) + tmpI),np.transpose(X)),Y)
    R = 1
    d = V.shape[0]
    beta = R * np.sqrt(math.log(np.linalg.det(V))/(lamb**d * delta**2)) + np.sqrt(lamb)
    return newV,newX,newY,theta,beta

def get_reward(W,gama=1):
    rt = np.count_nonzero(W)
    return rt 



