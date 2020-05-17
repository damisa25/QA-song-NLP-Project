import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')
from nltk.tokenize import word_tokenize #divide strings into lists of substrings
from nltk.corpus import stopwords #stopwords corpus
from nltk.stem.snowball import SnowballStemmer #An algorithm for suffix stripping
from collections import defaultdict #takes no arguments and provides the default value for a nonexistent key

try: reduce
except: from functools import reduce
try:    raw_input
except: raw_input = input

from pymongo import MongoClient
import uuid
# Create connection to MongoDB
client = MongoClient('mongodb+srv://dbDamisa:damisa.25@nlp-ipjo1.mongodb.net/test?retryWrites=true&w=majority')

db = client.db
docs_col = db.docs_db
words_col = db.words
inverted_col = db.invertedIndex_db

stop_word = set(stopwords.words('english')) #generate the most recent English stopword list
stemmer = SnowballStemmer("english") #Stemmers remove morphological affixes from words, leaving only the word stem.

question = "Who is the songwriter of Yummy song?" #Example

print(question)

""" Extract keywords : tokenization, POS-tagging, stop word removal, stemming"""
def extract_keys(question):
    tokens = word_tokenize(question)
    pos_tagging = nltk.pos_tag(tokens)
    pos_tagging = [(element[0].lower(),element[1]) for element in pos_tagging]
    pos_tagging = [(stemmer.stem(element[0]), element[1]) for element in pos_tagging if element[0] not in stop_word and '?' not in element[0]]
    print(pos_tagging)
    extracted_keywords = [element[0] for element in pos_tagging]
    print(extracted_keywords)
    return extracted_keywords

extracted_keywords = extract_keys(question)

""" Document Retrieval : matching keywords  from question with words from MongoDB"""
words = {}
for word in words_col.find({},{"_id":0}):
    words.update(word)

words = [v for v in words.keys()] #dict to set

docs = {}
for doc in docs_col.find({},{"_id":0}):
    docs.update(doc)

inverted_index = {}
for index in inverted_col.find({},{"_id":0}):
    inverted_index.update(index)

#print(index_dict)
def matchedkeywords(terms): # Searches full inverted index
    if not set(terms).issubset(words):
        return set()
    return reduce(set.intersection,
                  (inverted_index[term] for term in terms),
                  set(docs.keys()))

print('\nTerm Search for: ' + repr(extracted_keywords))
print(sorted(matchedkeywords(extracted_keywords)))
