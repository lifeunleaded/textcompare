#!/usr/bin/env python3
import gzip, sys, time,os
import numpy as np
import matplotlib.pyplot as plt
from saxonche import *
from Levenshtein import distance
os.makedirs('./report', exist_ok=True)
os.makedirs('./report/ncd', exist_ok=True)
os.makedirs('./report/lev', exist_ok=True)
cutoff = 0.06 # max distance to consider reuse
texts = [] # storage array for the texts to read
inputs = sys.argv[1:]

def cleantitles(xdmtitle):
    return str(xdmtitle).replace('title=','').strip('"')
if len(inputs) == 1 and  os.path.splitext(os.path.basename(inputs[0]))[1] == '.xml': # Single input arg ending in .xml is assumed to be a docbook article with sections
    print("Single XML as input, assuming sections are to be compared")
    proc=PySaxonProcessor(license=False)
    xp=proc.new_xslt30_processor()
    executable = xp.compile_stylesheet(stylesheet_file="textdiff.xsl")
    doc = proc.parse_xml(xml_file_name='samples/2.xml')
    executable.apply_templates_returning_file(xdm_node=doc,output_file="textdifftransformed.xml")
    output = proc.parse_xml(xml_file_name='textdifftransformed.xml')
    xproc = proc.new_xpath_processor()
    xproc.set_context(xdm_item=output)
    xproc.declare_namespace(prefix='d',uri='http://docbook.org/ns/docbook')
    xdmtextnames = list(xproc.evaluate('//d:section/@title'))
    xdmtexts = list(xproc.evaluate('//d:section/text()'))
    textnames = list(map(cleantitles, xdmtextnames))
    texts = list(map(str, xdmtexts))
else:
    textnames = list(map(lambda x: os.path.splitext(os.path.basename(x))[0],inputs))
    for filename in sys.argv[1:]: # i.e. you want to provide the list of files as input arguments, e.g. ./textdiffs2.py t1.xml t2.xml t3.xml...
        with open(filename,'r') as file:
            texts.append(file.read())

diffs = np.zeros((len(texts),len(texts))) # initiate a numpy matrix
levdiffs = np.zeros((len(texts),len(texts))) # initiate a numpy matrix

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
ncdtime = endtime-starttime

starttime = time.time()
for i in range(len(texts)):
    for j in range(len(texts)):
        levdiffs[i,j] = distance(texts[i],texts[j]) # populate the matrix with distances
endtime = time.time()
levtime = endtime-starttime
levminima = np.argmin(levdiffs,axis=1)
# Plot NCD heatmap
fig, ax = plt.subplots()
fig.set_size_inches(len(textnames), len(textnames))
im = ax.imshow(diffs,cmap="Wistia")
ax.set_xticks(np.arange(len(texts)), labels=textnames)
ax.set_yticks(np.arange(len(texts)), labels=textnames)
plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
         rotation_mode="anchor")
for i in range(len(texts)):
    for j in range(len(texts)):
        text = ax.text(j, i, "{:0.2f}".format(diffs[i, j].item()),
                       ha="center", va="center", color="b")
plt.savefig('report/ncd/similarities.png',bbox_inches="tight",dpi=300)
plt.close()

reportfile = open('report/index.html','w')
reportfile.write("""<html>
<head>
<title>Reuse report</title>
</head>
<body>
<h1>Normalized Compression Distance (NCD)</h1>
<p>Computation time: {}\n</p>
<img src="ncd/similarities.png" width="100%"/>""".format(ncdtime))

for textindex in range(len(texts)):
    fig, ax = plt.subplots()
    ax.bar(list(range(len(texts))),diffs[textindex])
    ax.set_xticks(np.arange(len(texts)), labels=textnames,rotation=90)
    plt.savefig('report/ncd/{}.png'.format(textnames[textindex]),bbox_inches="tight")
    plt.close()
    reportfile.write("<h2>Difference scores for {}</h2>\n".format(textnames[textindex]))
    reportfile.write('<img src="ncd/{}.png"/>\n'.format(textnames[textindex]))
    reportfile.write("<p>Closest by difference: {} (distance {})</p>".format(textnames[minima[textindex]], diffs[textindex,minima[textindex]]))
    if diffs[textindex,minima[textindex]] < cutoff:
        reportfile.write("<p>With cutoff {}, substition is possible</p>".format(cutoff))
    else:
        reportfile.write("<p>With cutoff {}, substition is not possible</p>".format(cutoff))
# Plot Levenshtein
fig, ax = plt.subplots()
fig.set_size_inches(len(textnames), len(textnames))
im = ax.imshow(levdiffs,cmap="Wistia")
ax.set_xticks(np.arange(len(texts)), labels=textnames)
ax.set_yticks(np.arange(len(texts)), labels=textnames)
plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
         rotation_mode="anchor")
for i in range(len(texts)):
    for j in range(len(texts)):
        text = ax.text(j, i, "{:0.2f}".format(levdiffs[i, j].item()),
                       ha="center", va="center", color="b")
plt.savefig('report/lev/similarities.png',bbox_inches="tight",dpi=300)
plt.close()
reportfile.write("""<h1>Levenshtein Distance</h1>
<p>Computation time: {}\n</p>
<img src="lev/similarities.png" width="100%"/>""".format(levtime))
for textindex in range(len(texts)):
    fig, ax = plt.subplots()
    ax.bar(list(range(len(texts))),levdiffs[textindex])
    ax.set_xticks(np.arange(len(texts)), labels=textnames,rotation=90)
    plt.savefig('report/lev/{}.png'.format(textnames[textindex]),bbox_inches="tight")
    plt.close()
    reportfile.write("<h2>Difference scores for {}</h2>\n".format(textnames[textindex]))
    reportfile.write('<img src="lev/{}.png"/>\n'.format(textnames[textindex]))
    reportfile.write("<p>Closest by difference: {} (distance {})</p>".format(textnames[levminima[textindex]], levdiffs[textindex,levminima[textindex]]))

        
reportfile.write("""</body>
</html>""")


