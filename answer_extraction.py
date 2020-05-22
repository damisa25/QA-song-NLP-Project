""" Answer Extraction : POS tagging and NER """
import nltk 
import re
import spacy 

from pprint import pprint as pp
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict, Counter
from nltk.stem import WordNetLemmatizer
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

ne = spacy.load('en_core_web_sm')
lemmatizer = WordNetLemmatizer()
nltk.download('stopwords')
q_words = ['What', 'Where', 'When', 'Who', 'Why', 'How','what', 'where', 'when', 'who', 'why', 'how']
remove = ["?", "-",".",",","'","[","]","(",")","!","``","/",";",":","‘" ]
stop_word = set(stopwords.words('english'))


""" Named Entity : from Question and text file"""
def named_entities(question, sentences):
    """ Named entities in question """
    ner_question = []
    question_ne = ne(str(question))
    for ent in question_ne.ents: 
        ner_question.append((str(ent), ent.label_))
    #pp(ner_question)
    """ Named entities in sentences """
    ner_sentence = []
    ner_word = []
    for sentence in sentences:
        ne_sentence = ne(str(sentence))
        for ent in ne_sentence.ents: 
            ner_word.append((str(ent), ent.label_))
        ner_sentence.append(ner_word)
        ner_word=[]
    #pp(ner_sentence)
    return ner_question,ner_sentence

def pos_tagged_docs(sentences):

    lemmatizer = WordNetLemmatizer()
    pos_sentences = defaultdict(list)
    pos_words = defaultdict(list)
    i = 0
    for sentence in sentences:
        for sent in nltk.sent_tokenize(sentence):
            text = nltk.word_tokenize(sent)
            for value, tag in nltk.pos_tag(text, tagset='universal'):
                if value not in stop_word and '.' not in value and ',' not in value and value not in q_words and value not in remove:    
                    value = value.lower()
                    pos_words[tag].append(lemmatizer.lemmatize(value))
        pos_sentences[i].append(dict(pos_words))
        pos_words = defaultdict(list)
        i+=1

    return dict(pos_sentences)
#pp(dict(infos))

def second_match_pos(dict_value,pos_question,key_s):
    matched_index = []
    key = []
    for key_q, value_q in pos_question.items():
        match = lambda : True if not any(val in dict_value[key_q] for val in value_q) else False
        match = bool(match)
        if match == True:
            key.append(key_s)
   
    #pp(matched_index)
    return matched_index


def check_match_pos(pos_question, pos_sentences):
    matched_index = []
    key = []
    for key_s,value_s in pos_sentences.items():
        for value in value_s:
            dict_value = dict(value)
            try:
                for key_q, value_q in pos_question.items():
                    if all(val in dict_value[key_q] for val in value_q):
                        key.append(key_s)
            except KeyError:
                key = second_match_pos(dict_value,pos_question,key_s)
    counter1 = Counter(key)
    matched_index = [item for item, count in counter1.most_common(1)]

    return matched_index


""" Matched POS tagging and check Named Entity"""
def answer_extraction(question, pos_question, filename_extracted):
    global counter
    with open('songs/'+filename_extracted+'.txt', 'r') as f:
        doc = f.read()

    
    sentences = nltk.sent_tokenize(doc)

    ner_question, ner_sentences = named_entities(question, sentences)
    pos_sentences = pos_tagged_docs(sentences)
 
    matched_index = check_match_pos(pos_question, pos_sentences)
    """ Extract Answer """
    if len(matched_index) > 1:
        ans_ne = []
        most_ne = []
        for index in matched_index:
            matched_sentence_ne = ner_sentences[index]
            lyric = 'lyrics'
            if lyric in sentences[index]:
                ans_lyric = sentences[index:]
                ans_lyric = "\n".join(ans_lyric)
                return ans_lyric  
            if any(ne_word in matched_sentence_ne for ne_word in ner_question):
                for m in matched_sentence_ne:
                    most_ne.append(m[1])
                counter = Counter(most_ne)
                most_ne_occur = [word for word, words in counter.most_common(1)]
                for j in matched_sentence_ne:
                    if j[1] in most_ne_occur:
                        ans_ne.append(j[0])
        ans_ne = ','.join(ans_ne)
        return ans_ne
    else:
        for index in matched_index:
            lyric = 'lyrics'
            if lyric in sentences[index]:
                ans_lyric = sentences[index:]
                ans_lyric = "\n".join(ans_lyric)
                return ans_lyric  
            answer_sentence = sentences[index]
            return answer_sentence
            
