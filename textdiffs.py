#!/usr/bin/env python3
import gzip, sys, time
import numpy as np
texts = [] # storage array for the texts to read
cutoff = 0.06 # max distance to consider reuse
for filename in sys.argv[1:]: # i.e. you want to provide the list of files as input arguments, e.g. ./textdiffs2.py t1.xml t2.xml t3.xml...
    with open(filename,'r') as file:
        texts.append(file.read())

diffs = np.zeros((len(texts),len(texts))) # initiate a numpy matrix

# NCD as a function
def ncd(x1,x2):
    Cx1 = len(gzip.compress(x1.encode()))
    Cx2 = len(gzip.compress(x2.encode()))
    x1x2 = " ".join([x1,x2])
    Cx1x2 = len(gzip.compress(x1x2.encode()))
    return (Cx1x2-min(Cx1, Cx2))/max(Cx1, Cx2)
starttime = time.time()
for i in range(len(texts)):
    for j in range(len(texts)):
        diffs[i,j] = ncd(texts[i],texts[j]) # populate the matrix with distances

normdiffs = diffs + np.eye(len(texts)) # add an identity matrix to offset suggesting yourself as reuse
minima = np.argmin(normdiffs,axis=1) # get the lowest distances in the matrix for each text
endtime = time.time()
print("Processing time for NCD: {}\n".format(endtime-starttime))
print("Based on NCD approximation of Kolmogorov complexity, apart from itself:\n")
for i in range(len(np.argmin(normdiffs,axis=1))):
    print("\t* Text {} is most similar to text {}, distance metric {}\n".format(sys.argv[i+1],sys.argv[minima[i]+1],diffs[i,minima[i]]))
    if diffs[i,minima[i]] < cutoff:
        print("\t\tWith a defined cutoff distance of {}, we could recommend reusing {} instead of {}\n".format(cutoff,sys.argv[minima[i]+1],sys.argv[i+1]))
    else:
        print("\t\tWith a defined cutoff distance of {}, we cannot identify a substitution candidate for {}\n".format(cutoff,sys.argv[i+1]))
