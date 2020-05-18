import nltk
import ssl
from pprint import pprint as pp

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
from collections import defaultdict

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
words_col = db.words_db
inverted_col = db.invertedIndex_db

stop_word = set(stopwords.words('english'))
stemmer = SnowballStemmer("english")

question = "Who is the songwriter of Yummy song?" #Example

print(question)

""" Extract keywords : tokenization, POS-tagging, stop word removal, stemming"""
def extract_keys(question):
    tokens = word_tokenize(question)
    pos_tagging = nltk.pos_tag(tokens)
    pos_tagging = [(element[0].lower(),element[1]) for element in pos_tagging]
    pos_tagging = [(stemmer.stem(element[0]), element[1]) for element in pos_tagging if element[0] not in stop_word and '?' not in element[0] and ',' not in element[0]]
    print(pos_tagging)
    extracted_keywords = [element[0] for element in pos_tagging]
    print(extracted_keywords)
    return extracted_keywords

extracted_keywords = extract_keys(question)

""" Document Retrieval : matching keywords  from question with words from MongoDB"""
#Query words from mongoDB
words = {}
for word in words_col.find({},{"_id":0}):
    words.update(word)

words = [v for v in words.keys()]   #Dictionary to Set

#Query name of each text file that contain words from mongoDB
docs = {}
for doc in docs_col.find({},{"_id":0}):
    docs.update(doc)

#Query inverted index dictionary from mongoDB
inverted_index = {}
for index in inverted_col.find({},{"_id":0}):
        inverted_index.update(index)


terms = [ term for term in extracted_keywords if term in words]

# Searches inverted index dictionary
def matchedkeywords(terms): 
    if not set(terms).issubset(words):
        return set()
    return reduce(set.intersection,
                  (set(x[0] for x in txtindx)
                   for term, txtindx in inverted_index.items()
                   if term in terms),
                  set(docs.keys()))

print('\nTerm Search for: ' + repr(terms))
relevant_docs = sorted(matchedkeywords(terms))
print(relevant_docs)

""" File Reranking : find out between query keywords and all text files
                     Using Jaccard Similarity function"""
def jaccard_similarity(extractedWords, fileWords):
    words_query = set(extractedWords)
    words_file = set(fileWords)
    score = len(words_query.intersection(words_file)) / len(words_query.union(words_file))
    return score

def file_reranking(extractedWords, relevant_docs):
    pp(extractedWords)
    words_in_file= []
    score = []
    score_doc = []
    for doc in relevant_docs:
        for key, value in docs.items():
            if key == doc:
                words_in_file = value
                score_doc.append(key)
                score.append(jaccard_similarity(extractedWords, words_in_file))
    max_score_file = max(zip(score,score_doc))
    return max_score_file[1]


pp(file_reranking(terms, relevant_docs)) 


