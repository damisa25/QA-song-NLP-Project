""" Part 1 : text processing by doing inverted index dictionary"""
from pprint import pprint as pp
from glob import glob
from collections import Counter

from pymongo import MongoClient
import uuid
# Create connection to MongoDB
client = MongoClient('mongodb+srv://dbDamisa:damisa.25@nlp-ipjo1.mongodb.net/test?retryWrites=true&w=majority')

db = client.db
docs_col = db.docs_db
words_col = db.words
inverted_col = db.invertedIndex_db

import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

try: reduce
except: from functools import reduce
try:    raw_input
except: raw_input = input


stop_word = set(stopwords.words('english'))
stemmer = SnowballStemmer("english")

"""Tokenization, Stop words removal, Stemming """
def parsetexts(fileglob='Songs/T*.txt'): #T1.txt-T20.txt
    docs, words = {}, set()
    #Extract words from txt
    for txtfile in glob(fileglob):
        with open(txtfile, 'r') as f:
            txt = word_tokenize(f.read())
            txt = [stemmer.stem(element).lower() for element in txt if not element in stop_word and '.' not in element] 
            words |= set(txt) #words appear in all files
            docs[txtfile.split('/')[-1].replace('.txt', '')] = txt #words in each text file
    return docs, words

docs, words = parsetexts()
words = dict.fromkeys(words, 0)

""" Index term dictionary """
def inverted_index_dict(docs,words):
    inverted_index = {}
    for word in words:
        for txt, wrds in docs.items():
            if word in wrds:
                inverted_index.setdefault(word, []).append(txt)
    return inverted_index

inverted_index = inverted_index_dict(docs,words)

""" Inserting into MongoDB"""
try:
    docs_col.insert_one(docs)
    words_col.insert_one(words)
    inverted_col.insert_one(inverted_index)
except: print('This connect or insert is wrong')
