import numpy as np

def PCA(M,k):
        mt=M.transpose()
        #make the varables as row data 
        means = np.mean(mt,axis=1)
        mt_zeromean = (mt.transpose()-means).transpose()
        print "zero-mean done."
        #get zero-mean matrix of orginal data
        mt_cov = np.cov(mt_zeromean)
        print "cov done."
        #get covariance matrix
        #C=np.dot(mt,M) #Not important, this is only for computing SVD to check result 
        w,v = np.linalg.eig(mt_cov)
        print "eigen done."
        #get eigenvalues and eigenvectors
        indOrder = np.argsort(w)
        #sort eigenvalues and get corrsponding indices
        k_top_order = indOrder[-1-k+1:]
        k_top_order = k_top_order[::-1]
        pc = v[:,k_top_order]
        #get k top eigenvectors according to the sorted order of eigenvalues
        #return(pc)
        newm = np.dot(M,pc)
        return newm  #return the dimensional-decreased matrix

dim = 10
# perform pca for app feature
data = []
countr = 0
id = []
with open("../app_feature_origin.txt",'r') as f:
    for line in f:
        countr += 1
        l = line.strip().rstrip(',').split(',')
        l = list(map(float, l))
        data.append(int(l[1:]))
        id.append(l[0])
    f.close()

A = np.asarray(data,dtype=np.float)
C = PCA(A,dim)

with open("../app_feature.txt",'w') as f:
    for i in range(0,countr):
        f.write(str(id[i])) 
        for j in range(0,100):
            f.write(',')
            f.write(str(C[i,j].real))
        f.write('\n')
    f.close()
print "app_feature done."

# perform pca for user feature
data = []
countr = 0
id = []
with open("../user_feature_origin.txt",'r') as f:
    for line in f:
        countr += 1
        l = line.strip().rstrip(',').split(',')
        l = list(map(float, l))
        data.append(l[1:])
        id.append(int(l[0]))
    f.close()

        
A = np.asarray(data,dtype=np.float)
C = PCA(A,dim)

with open("../user_feature.txt",'w') as f:
    for i in range(0,countr):
        f.write(str(id[i]))
        for j in range(0,100):
            f.write(',')
            f.write(str(C[i,j].real))
        f.write('\n')
    f.close()
print "user_feature done."
