import nltk
import spacy
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
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
#from collections import defaultdict

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
lemmatizer = WordNetLemmatizer()
q_words = ['What', 'Where', 'When', 'Who', 'Why', 'How','what', 'where', 'when', 'who', 'why', 'how']

question = "Who is the songwriter of Yummy?" #Example

""" Extract keywords : tokenization, POS-tagging, stop word removal, stemming"""
def extract_keys(question):
    """ Keywords """
    tokens_keywords = word_tokenize(question)
    extracted_keywords = [lemmatizer.lemmatize(element).lower() for element in tokens_keywords 
                            if element not in stop_word and '?' not in element and ',' not in element and element not in q_words] 

    """ POS tagging answer """
    pos_question = defaultdict(list)
    for value, tag in nltk.pos_tag(extracted_keywords, tagset='universal'):
        pos_question[tag].append(value)

    return extracted_keywords, dict(pos_question)
    

extracted_keywords, pos_question = extract_keys(question)
pp(extracted_keywords)
pp(pos_question)

   
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

"""File Reranking : find out between query keywords and all text files
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

extract_file = file_reranking(terms, relevant_docs)
pp(extract_file) 


