# textcompare
Experimental PoC to piggyback on the NCD text comparison used in [this paper](https://aclanthology.org/2023.findings-acl.426.pdf). This, however, tries to use it to just measure the distance between strings to see if they can serve as suggestions for each other, and omits labelling and categorization using k-nearest-neighbor.

To run, simply do ./textdiffs.py samples/*

TODO: Visualizations