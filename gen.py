#!/usr/bin/env python
import nltk
from nltk.parse.generate import generate
import random

grammar = nltk.CFG.fromstring("""
    S -> N "is" AP
    N -> "MLH" | "compression" | "Pod 4.2.0"
    AP -> A "because" S | A "but" S | AV A | A
    ADV -> "extremely" | "the most"
    A -> "cool" | "wonderful" | "spectacular"
""")

# rd_parser = nltk.RecursiveDescentParser(grammar)
# for p in rd_parser.parse(sent):
    # print(p)

sents = list(generate(grammar, depth=8, n=10000))

with open("compressme.txt",'w') as f:
    size = 0
    while size < 102400: 
        rand_sent = random.choice(sents)
        line = " ".join(rand_sent) + "!\n"
        size += len(line)
        f.write(line)
