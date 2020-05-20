import question_preprocessing 
import answer_extraction
import sys
from pymongo import MongoClient
from pprint import pprint as pp
import uuid
""" Create connection to MongoDB database """
client = MongoClient('mongodb+srv://dbDamisa:damisa.25@nlp-ipjo1.mongodb.net/test?retryWrites=true&w=majority')

db = client.db
docs_col = db.docs_db
words_col = db.words_db
inverted_col = db.invertedIndex_db

question = "Who is the songwriter of Yummy?" #Example

extracted_keywords, pos_question = question_preprocessing.extract_keys(question)
#pp(extracted_keywords)
#pp(pos_question)
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

def main():
    terms =[]
    for term in extracted_keywords:
        if term in words:
            terms.append(term)
    if not term:
        pp('Please give more informations')
        sys.exit()

    filename_extracted = question_preprocessing.file_reranking(extracted_keywords,terms,words,docs,inverted_index)
    answer = answer_extraction.answer_extraction(question, pos_question, filename_extracted )
    pp(answer)

if __name__ == '__main__':
    main()