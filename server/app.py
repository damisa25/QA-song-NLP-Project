from flask import Flask, jsonify, request
from flask_cors import CORS
import question_preprocessing 
import answer_extraction
import sys
from pymongo import MongoClient
from flask_pymongo import PyMongo
from pprint import pprint as pp
import uuid


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://dbDamisa:damisa.25@nlp-ipjo1.mongodb.net/test?retryWrites=true&w=majority"
mongo = PyMongo(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

""" Create connection to MongoDB database """
"""client = MongoClient('mongodb+srv://dbDamisa:damisa.25@nlp-ipjo1.mongodb.net/test?retryWrites=true&w=majority')

db = client.db
docs_col = db.docs_db
words_col = db.words_db
inverted_col = db.invertedIndex_db"""
# sanity check route
 #Example

#pp(extracted_keywords)
#pp(pos_question)
#Query words from mongoDB


@app.route('/qa', methods=['GET', 'POST'])
def question_answer():
    
    if request.method == 'POST':
        question = request.get_data()
        extracted_keywords, pos_question = question_preprocessing.extract_keys(question)
        words = {}
        for word in mongo.db.words_db.find({},{"_id":0}):
            words.update(word)

        words = [v for v in words.keys()]   #Dictionary to Set

        #Query name of each text file that contain words from mongoDB
        docs = {}
        for doc in mongo.db.docs_db.find({},{"_id":0}):
            docs.update(doc)

        #Query inverted index dictionary from mongoDB
        inverted_index = {}
        for index in mongo.db.invertedIndex_db.find({},{"_id":0}):
            inverted_index.update(index)
        terms =[]
        for term in extracted_keywords:
            if term in words:
                terms.append(term)
        if not term:
            response_object ={'ans': 'Please give more informations'}

        filename_extracted = question_preprocessing.file_reranking(extracted_keywords,terms,words,docs,inverted_index)
        answer = answer_extraction.answer_extraction(question, pos_question, filename_extracted )
        response_object ={'ans': answer}
    else:
        response_object ={'ans': ''}
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()