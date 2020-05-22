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

questions = [
            "What is the lengths of Yummy?", #10 T0Yummy
            "Who is the singer of Yummy?",
            "What is the genre of Yummy?",
            "Who is the songwriter of Yummy",
            "When was Yummy released?",
            "Who is the music copyright owner of Yummy?",
            "Who is the record label of Yummy?",
            "What is the lyrics of Yummy?",
            "What is the album of Yummy?",
            "What is the nationality of the singer that is the owner of Yummy?",
            # "What is the lengths of Comethru?", #20 T1Comethru
            # "Who is the artist of Comethru?",
            # "What is the genre of Comethru?",
            # "Who is the songwriter of Comethru",
            # "When was Comethru released?",
            # "Who is the music copyright owner of Comethru?",
            # "Who is the record label of Comethru?",
            # "What is the lyrics of Comethru?",
            # "What is the album of Comethru?",
            # "What is the nationality of the singer that is the owner of Comethru?",
            # "What is the lengths of Life of the Party?", #30 T2Life of the Party
            # "Who is the singer of Life of the Party?",
            # "What is the genre of Life of the Party?",
            # "Who is the songwriter of Life of the Party",
            # "When was Comethru released?",
            # "Who is the music copyright owner of Life of the Party?",
            # "Who is the record label of Life of the Party?",
            # "What is the lyrics of Life of the Party?",
            # "What is the album of Life of the Party?",
            # "What is the nationality of the singer that is the owner of Life of the Party?",
            # "What is the lengths of Change?", #40 T16Change
            # "Who is the singer of Change?",
            # "What is the genre of Change?",
            # "Who is the songwriter of Change",
            # "When was Comethru released?",
            # "Who is the music copyright owner of Change?",
            # "Who is the record label of Change?",
            # "What is the lyrics of Change?",
            # "What is the album of Change?",
            # "What is the nationality of the singer that is the owner of Change?",
            # "What is the lengths of Numb?", #50 T20Numb
            # "Who is the singer of Numb?",
            # "What is the genre of Numb?",
            # "Who is the songwriter of Numb",
            # "When was Numb released?",
            # "Who is the music copyright owner of Numb?",
            # "Who is the record label of Numb?",
            # "What is the lyrics of Numb?",
            # "What is the album of Numb?",
            # "What is the nationality of the singer that is the owner of Numb?",
            # "What is the lengths of Teeth?", #60 T3Teeth
            # "Who is the singer of Teeth?",
            # "What is the genre of Teeth?",
            # "Who is the songwriter of Teeth",
            # "When was Teeth released?",
            # "Who is the music copyright owner of Teeth?",
            # "Who is the record label of Teeth?",
            # "What is the lyrics of Teeth?",
            # "What is the album of Teeth?",
            # "What is the nationality of the singer that is the owner of Teeth?",
            # "What is the lengths of Head Held High?", #60 T6Head Held High
            # "Who is the singer of Head Held High?",
            # "What is the genre of Head Held High?",
            # "Who is the songwriter of Head Held High",
            # "When was Head Held High released?",
            # "Who is the music copyright owner of Head Held High?",
            # "Who is the record label of Head Held High?",
            # "What is the lyrics of Head Held High?",
            # "What is the album of Head Held High?",
            # "What is the nationality of the singer that is the owner of Head Held High?",
            # "What is the lengths of In the end?", #70 T15In the end
            # "Who is the singer of In the end?",
            # "What is the genre of In the end?",
            # "Who is the songwriter of In the end",
            # "When was In the end released?",
            # "Who is the music copyright owner of In the end?",
            # "Who is the record label of In the end?",
            # "What is the lyrics of In the end?",
            # "What is the album of In the end?",
            # "What is the nationality of the singer that is the owner of In the end?"
            # "What is the lengths of Afterlife?", #80 T5Afterlife
            # "Who is the singer of Afterlife?",
            # "What is the genre of Afterlife?",
            # "Who is the songwriter of Afterlife",
            # "When was Afterlife released?",
            # "Who is the music copyright owner of Afterlife?",
            # "Who is the record label of Afterlife?",
            # "What is the lyrics of Afterlife?",
            # "What is the album of Afterlife?",
            # "What is the nationality of the singer that is the owner of Afterlife?",
            # "What is the lengths of Hey Jude?", #90 T9Hey Jude
            # "Who is the singer of Hey Jude?",
            # "What is the genre of Hey Jude?",
            # "Who is the songwriter of Hey Jude",
            # "When was Hey Jude released?",
            # "Who is the music copyright owner of Hey Jude?",
            # "Who is the record label of Hey Jude?",
            # "What is the lyrics of Hey Jude?",
            # "What is the album of Hey Jude?",
            # "What is the nationality of the singer that is the owner of Hey Jude?",
            # "What is the lengths of Hydrocodone?", #100 T8Hydrocodone
            # "Who is the singer of Hydrocodone?",
            # "What is the genre of Hydrocodone?",
            # "Who is the songwriter of Hydrocodone",
            # "When was Hydrocodone released?",
            # "Who is the music copyright owner of Hydrocodone?",
            # "Who is the record label of Hydrocodone?",
            # "What is the lyrics of Hydrocodone?",
            # "What is the album of Hydrocodone?",
            # "What is the nationality of the singer that is the owner of Hydrocodone?",
            ]



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
        terms =[]
        for term in extracted_keywords:
            if term in words:
                terms.append(term)
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
