# textcompare
Experimental PoC to piggyback on the NCD text comparison used in [this paper](https://aclanthology.org/2023.findings-acl.426.pdf). This, however, tries to use it to just measure the distance between strings to see if they can serve as suggestions for each other, and omits labelling and categorization using k-nearest-neighbor.

To run, simply do `./textdiffs.py samples/*`

```
Processing time for NCD: 0.0029735565185546875

Based on NCD approximation of Kolmogorov complexity, apart from itself:

        * Text samples/t1.xml is most similar to text samples/t2.xml, distance metric 0.031746031746031744

                With a defined cutoff distance of 0.06, we could recommend reusing samples/t2.xml instead of samples/t1.xml

        * Text samples/t2.xml is most similar to text samples/t1.xml, distance metric 0.031746031746031744

                With a defined cutoff distance of 0.06, we could recommend reusing samples/t1.xml instead of samples/t2.xml

        * Text samples/t3.xml is most similar to text samples/t5.xml, distance metric 0.23157894736842105

                With a defined cutoff distance of 0.06, we cannot identify a substitution candidate for samples/t3.xml

        * Text samples/t4.xml is most similar to text samples/t5.xml, distance metric 0.07291666666666667

                With a defined cutoff distance of 0.06, we cannot identify a substitution candidate for samples/t4.xml

        * Text samples/t5.xml is most similar to text samples/t1.xml, distance metric 0.05263157894736842

                With a defined cutoff distance of 0.06, we could recommend reusing samples/t1.xml instead of samples/t5.xml
```

TODO: Visualizations