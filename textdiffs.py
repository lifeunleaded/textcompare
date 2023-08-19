#!/usr/bin/env python3
import gzip, sys, time,os
import numpy as np
import matplotlib.pyplot as plt
# from saxonche import *
os.makedirs('./report', exist_ok=True)
cutoff = 0.06 # max distance to consider reuse
texts = [] # storage array for the texts to read
inputs = sys.argv[1:]
if len(inputs) == 1 and  os.path.splitext(os.path.basename(inputs[0]))[1] == '.xml':
    print("Single XML as input, assuming sections are to be compared")
    # proc=PySaxonProcessor(license=False)
    # xslt30proc=proc.new_xslt30_processor()
else:
    textnames = list(map(lambda x: os.path.splitext(os.path.basename(x))[0],inputs))
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

fig, ax = plt.subplots()
im = ax.imshow(diffs,cmap="Wistia")
ax.set_xticks(np.arange(len(texts)), labels=textnames)
ax.set_yticks(np.arange(len(texts)), labels=textnames)
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
for i in range(len(texts)):
    for j in range(len(texts)):
        text = ax.text(j, i, "{:0.4f}".format(diffs[i, j].item()),
                       ha="center", va="center", color="b")
plt.savefig('report/similarities.png',bbox_inches="tight")
plt.close()

reportfile = open('report/index.html','w')
reportfile.write("""<html>
<head>
<title>Reuse report</title>
</head>
<body>
<h1>Similarity heatmap</h1>
<img src="similarities.png"/>""")

for textindex in range(len(texts)):
    fig, ax = plt.subplots()
    ax.bar(list(range(len(texts))),diffs[textindex])
    ax.set_xticks(np.arange(len(texts)), labels=textnames,rotation=45)
    plt.savefig('report/{}.png'.format(textnames[textindex]),bbox_inches="tight")
    plt.close()
    reportfile.write("<h2>Difference scores for {}</h2>\n".format(textnames[textindex]))
    reportfile.write('<img src="{}.png"/>\n'.format(textnames[textindex]))
    reportfile.write("<p>Closest by difference: {} (distance {})</p>".format(textnames[minima[textindex]], diffs[textindex,minima[textindex]]))
    if diffs[textindex,minima[textindex]] < cutoff:
        reportfile.write("<p>With cutoff {}, substition is possible</p>".format(cutoff))
    else:
        reportfile.write("<p>With cutoff {}, substition is not possible</p>".format(cutoff))

reportfile.write("""</body>
</html>""")


