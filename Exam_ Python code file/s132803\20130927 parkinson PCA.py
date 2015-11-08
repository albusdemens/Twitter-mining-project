# -*- coding: utf-8 -*-

# The script downloads, imports and analyses (via correlation matrix and PCA) a dataset dealing with Parkinson's decease.
# Four plots are created:
#   1: Correlation matrix
#   2: Cumulative pct. of total variation explained by the principal components
#   3: The dataset projected onto the first seven principal components and plottet via Parallel coordinates
#   4: The dataset projected onto the first seven principal components and plottet against each other
#
# The dataset is composed of a range of biomedical voice measurements from 31 people, 23 with Parkinson’s disease (PD). 
# The dataset has 23 attributes and each of the 31 people in the dataset has been recorded a number of times. 
# See: http://archive.ics.uci.edu/ml/datasets/Parkinsons for more info

import csv, numpy as np,scipy.linalg as linalg, urllib2
from pylab import plot,yticks,legend,figure,subplot,show,xlabel,xticks,ylabel,hold,imshow,cm,colorbar
from scipy.stats import zscore

### DOWNLOAD DATASET AND FINALIZE DATA FOR ANALYSIS
# Download the "Parkinsons Data Set" from UCI, then load the CSV dataset and copy all but first line to a matrix: data
reader = csv.reader(urllib2.urlopen('http://archive.ics.uci.edu/ml/machine-learning-databases/parkinsons/parkinsons.data'),delimiter=',')
read = list(reader)
data = np.matrix(read[1:len(read)])

# Itterate over all rows in the matrix to extract the attribute: "patientId" and "testId" from the column "name"
patientId = np.zeros((len(data),1)).astype(int)
testId = np.empty((len(data),1)).astype(int)
j = 0
for i in data[:,0]:
        patientId[j] = i[0,0].split('_')[2][1:]
        testId[j] = i[0,0].split('_')[3]
        j = j+1

# Create a y matrix with the 'status' column from the dataset
y = data[:,17].astype(int)
# Create the X matrix with all data from the dataset except the 'status' (column 17) and 'name' (column 0) columns
X = np.delete(data,[0,17],1).astype(float)
# Finalize the X matrix by adding the patientId and testId
X = np.hstack([patientId,testId, X])
# Create a vector with attribute names 
attributeNames = ['patientId','testId']+read[0][1:17]+read[0][18:24]
N = len(y) # Number of obeservations
M = len(attributeNames) # Number of attributes
# Normalize X to have zero mean and standart deviation of one
X_standarized = zscore(X, ddof=0)


### PLOT OF SUMMARY STATS
# 1: Plot correlation matrix
figure(figsize=(10,10))
imshow(np.corrcoef(X_standarized.transpose()[2:]), interpolation='nearest',  cmap=cm.gray);
xticks(range(0,M+1-3),attributeNames[2:],rotation=90)
yticks(range(0,M+1-3),attributeNames[2:])
colorbar()
show()



### PRINCIPAL COMPONENT ANALISYS
U,S,V = linalg.svd(X_standarized)
V = np.mat(V).T
U = np.mat(U)
# Project data onto principal component space
Z = X_standarized * V
# Number of principal components to be analysed
K = 7
# Classes to include in analysis 0: healty, 1: sick. Define colors for classes to be used in plots
n = [0,1]
color = ["g","r"]
# Replace X, attributeNames, and M
X = Z[:,:K]
attributeNames = ['PC{0}'.format(no) for no in range(1,K+1)]
M = K
C = len(n)



### PLOTS OF PCA

# 2: Plot: Cumulative pct. of total variation explained by the principal components
figure(figsize=(10,6))
attributeNames = ['PC{0}'.format(no) for no in range(1,len(S)+1)]
plot(np.cumsum(S)/sum(S))
xticks(range(0,len(S)+1),attributeNames,rotation=45)
ylabel("Cumulative pct. of total variation \nexplained by the principal components (PC)")
show()

# 3: Plot: the dataset projected onto the first seven principal components
figure(figsize=(10,6))
hold(True)
for c in range(C):
    c = C-c-1
    class_mask = (y==c).A.ravel() # binary mask to extract elements of class c
    plot(X[class_mask,:].transpose(),color=color[c])
    xticks(range(0,7),attributeNames)
ylabel("Coordinate value")
show()

# 4: Plot: the dataset projected onto the first seven principal components and plottet against each other
figure(figsize=(10,10))
hold(True)
for m1 in range(M):
    for m2 in range(M):
        subplot(M, M, m1*M + m2 + 1)
        for c in range(C):
            class_mask = (y==c).A.ravel()
            plot(X[class_mask,m2], X[class_mask,m1], '.',color=color[c])
            if m1==M-1: xlabel(attributeNames[m2]);
            else: xticks([]);
            if m2==0: ylabel(attributeNames[m1]);
            else: yticks([]);
legend(["Healthy","Sick"])
show()










