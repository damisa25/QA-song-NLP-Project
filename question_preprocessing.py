import nltk
import spacy
import uuid
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

try: reduce
except: from functools import reduce

from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
from pprint import pprint as pp
from pymongo import MongoClient
nltk.download('stopwords')
stop_word = set(stopwords.words('english'))

lemmatizer = WordNetLemmatizer()
q_words = ['What', 'Where', 'When', 'Who', 'Why', 'How','what', 'where', 'when', 'who', 'why', 'how']

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
    
   
""" Document Retrieval : matching keywords  from question with words from MongoDB"""
def matchedkeywords(terms,words, docs, inverted_index): 
    if not set(terms).issubset(words):
        return set()
    return reduce(set.intersection,
                  (set(x[0] for x in txtindx)
                   for term, txtindx in inverted_index.items()
                   if term in terms),
                  set(docs.keys()))


"""File Reranking : find out between query keywords and all text files
                     Using Jaccard Similarity function"""
def jaccard_similarity(extractedWords, fileWords):
    words_query = set(extractedWords)
    words_file = set(fileWords)
    score = len(words_query.intersection(words_file)) / len(words_query.union(words_file))
    return score

def file_reranking(extractedWords, terms, words, docs, inverted_index):
    relevant_docs = sorted(matchedkeywords(terms, words, docs, inverted_index))
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



