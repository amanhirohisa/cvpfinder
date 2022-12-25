#coding: UTF-8
import fileinput
from gensim.models.doc2vec import Doc2Vec
import sys
import numpy as np
from nltk.stem.porter import PorterStemmer as PS
import re


args = sys.argv
decimal_pattern = re.compile(r'[0-9]+')
ps = PS()

model = Doc2Vec.load(args[1])

# header
print("path", "name1", "name2", "range", "semantic_similarity", sep='\t')

def convert(words):
    tokens = words.lower()
    tokens = tokens.replace(',', ' ')
    tokens = decimal_pattern.sub(' <num> ', tokens)
    stemmed_tokens = []
    for token in tokens.split():
        if token.isdecimal():
            stemmed_tokens.append('<num>')
        else:
            stemmed_tokens.append(ps.stem(token))
    return stemmed_tokens

is_header = True
for line in fileinput.input(files='-'):
    if is_header:
        is_header = False
        continue
    line = line.strip()
    records = line.split('\t')
    path = records[0]
    name1 = records[1]
    name2 = records[2]
    scope = records[3]
    words1 = records[4]
    words2 = records[5]
    if name1 == name2:
        cossim = 1
    else:
        v1 = model.infer_vector(convert(words1))
        v2 = model.infer_vector(convert(words2))
        cossim = np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
    print(path, name1, name2, scope, cossim, sep='\t')
