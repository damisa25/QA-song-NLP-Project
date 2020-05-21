""" Part 1 : text processing by doing inverted index dictionary"""
import nltk
import re
import ssl
import pymongo

import uuid
from pprint import pprint as pp
from glob import glob
from collections import Counter
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict
from pymongo import MongoClient
from nltk.stem import WordNetLemmatizer

# Create connection to MongoDB
client = MongoClient('mongodb+srv://dbDamisa:damisa.25@nlp-ipjo1.mongodb.net/test?retryWrites=true&w=majority')

db = client.db
docs_col = db.docs_db
words_col = db.words_db
inverted_col = db.invertedIndex_db

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


nltk.download('stopwords')
lemmatizer = WordNetLemmatizer()
stop_word = set(stopwords.words('english'))
stemmer = SnowballStemmer("english")
remove = ["?", "-",".",",","'","[","]","(",")","!","``","/",";",":","‘","''" ]

"""Tokenization, Normalization, Stemming """
def parsetexts(fileglob='Songs/T*.txt'):
    docs, words = {}, set()
    #Extract words from txt
    for txtfile in glob(fileglob):
        with open(txtfile, 'r') as f:
            txt = word_tokenize(f.read())   # Word tokenization
            """pp('Word Tokenization')
            pp(txt)"""
            """Stop word removal, Lowercase, Stemming"""
            txt = [element.lower() for element in txt if not element in stop_word and element not in remove and '.' not in element] 
            txt=  [lemmatizer.lemmatize(ele) for ele in txt]
            """pp('Stop word removal and Stemming')
            pp(txt)"""
            words |= set(txt) #Words appear in all files
            docs[txtfile.split('/')[-1].replace('.txt', '')] = txt #Words in each text file
    return docs, words

docs, words = parsetexts()
#pp(docs)
words = dict.fromkeys(words, 0)  #

""" Index term dictionary """
def inverted_index_dict(docs,words):
    inverted_index = {}  
    for word in words:
        for txt, wrds in docs.items():
            if word in wrds:
                inverted_index.setdefault(word, []).append(txt)
    return inverted_index

inverted_index = inverted_index_dict(docs,words)
#pp(inverted_index)


""" Inserting into MongoDB """

try:
    docs_col.insert_one(docs)
    words_col.insert_one(words)
    inverted_col.insert_one(inverted_index)
except: print('This connect or insert is wrong')
