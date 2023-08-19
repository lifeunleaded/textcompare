# textcompare
[License](LICENSE)

Experimental PoC to piggyback on the NCD text comparison used in [this paper](https://aclanthology.org/2023.findings-acl.426.pdf). This, however, tries to use it to just measure the distance between strings to see if they can serve as suggestions for each other, and omits labelling and categorization using k-nearest-neighbor.

Prerequisites:
numpy, saxonche, python-Levenshtein (pip installable)

`textdiffs.py` takes one more more input file names as argument. If there is only one and it ends in .xml
it is assumed to be a docbook document where the sections are to be compared. If there are multiple files,
the files are compared as text.

To run, simply do `./textdiffs.py inputfile1...`

The result is a directory `report/` with an `index.html` contains the similarity report, first for NCD, followed by Levenshtein.