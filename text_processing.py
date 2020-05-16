""" Part 1 : text processing by doing inverted index dictionary"""
from pprint import pprint as pp
from glob import glob

from pymongo import MongoClient
import uuid
# Create connection to MongoDB
client = MongoClient('mongodb+srv://dbDamisa:<damisa.25>@nlp-ipjo1.mongodb.net/test?retryWrites=true&w=majority')

db = client.db
collection = db.invertedIndex_db


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
def parsetexts(fileglob='Songs/T*.txt'):
    texts, words = {}, set()
    #Extract words from txt
    for txtfile in glob(fileglob):
        with open(txtfile, 'r') as f:
            txt = word_tokenize(f.read())
            txt = [stemmer.stem(element).lower() for element in txt if not element in stop_word] 
            words |= set(txt) #words appear in all files
            texts[txtfile.split('/')[-1]] = txt #words in each text file
    return texts, words

texts, words = parsetexts()
print('\nTexts')
pp(texts)
print('\nWords')
pp(sorted(words))

""" Index term dictionary """
index_dict = {}  
for word in words:
    for txt, wrds in texts.items():
        if word in wrds:
            index_dict.setdefault(word, []).append(txt)


print('\nInverted Index')
pp(index_dict)

try:
    collection.insert_one(index_dict)
except:
    print('This connect or insert is wrong')
#result = collection.insert_one(index_dict)
#print(result)

""" Searching key in inverted index """
def termsearch(terms): # Searches simple inverted index
        try:
            for term in terms:
                index_dict[term]
                x = sorted(set(texts.keys()))
            return x    #key exists in dictionary
        except KeyError:
            return sorted(set(texts.keys()))    #key doesn't exists in dictionary


terms = [ "singer", "record","sasha"]
terms = [element.lower() for element in terms] 
print('\nTerm Search for: ' + repr(terms))
pp(termsearch(terms))
