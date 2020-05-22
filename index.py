import question_preprocessing 
import answer_extraction
import sys
import certifi
from pymongo import MongoClient
from pprint import pprint as pp
from collections import defaultdict
import uuid
""" Create connection to MongoDB database """

client = MongoClient('mongodb+srv://dbDamisa:damisa.25@nlp-ipjo1.mongodb.net/test?retryWrites=true&w=majority')

db = client.db
docs_col = db.docs_db
words_col = db.words_db
inverted_col = db.invertedIndex_db

questions = ["What is the lengths of Yummy?",
            "Who is the singer of Yummy?",
            "What is the genre of Yummy?", 
            "Who is the songwriter of Yummy", 
            "When was Yummy released?", 
            "Who is the song copyright owner of Yummy?",
            "Who is the record label of Yummy?",
            "What is the lyrics of Yummy?",
            "What is the album of Yummy?",
            "What is the nationality of the singer that is the owner of Yummy?"] #Example



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
   
    for question in questions:
        extracted_keywords, pos_question = question_preprocessing.extract_keys(question)
        pp(extracted_keywords)
        terms =[]
        for term in extracted_keywords:
            if term in words:
                terms.append(term)
        pp(terms)
        if not term:
            print('\nAnswer of\t'+question+'\n')
            pp('Please give more informations')
            sys.exit()
        
        filename_extracted = question_preprocessing.file_reranking(extracted_keywords,terms,words,docs,inverted_index)
        if not filename_extracted:
            answer = 'Sorry,this program has no information'
        else:
            pos_question_check = defaultdict(list)
            for tag,value in pos_question.items():
                for v in value:
                    if v in docs[filename_extracted]:
                        pos_question_check[tag].append(v)
            answer = answer_extraction.answer_extraction(question, dict(pos_question_check), filename_extracted )
        if answer:
            print('\nAnswer of\t'+question+'\n')
            pp(answer)
            print('+++++++++++++++++++++++++++++++')
        else:
            print('\nAnswer of\t'+question+'\n')
            pp('Sorry, No answer')
            print('+++++++++++++++++++++++++++++++')
    #pp(filename_extracted)

if __name__ == '__main__':
    main()