#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from com import Com
from trends import Trend
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import string
import matplotlib.pyplot as plt
#-----------------------------------------------------------------------
STOP_WORDS = ['the', 'you', 'and', 'to', 'like', 'that', 'it', 'of', 'in', 'was', 
'is', 'my', 'im', 'know', 'this', 'on', 'its', 'just', 'what', 'me', 'dont', 'they', 
'he', 'have', 'do', 'so', 'for', 'we', 'be', 'all', 'but', 'with', 'your', 'not', 
'thats', 'get', 'up', 'are', 'at', 'out', 'no', 'right', 'go', 'if', 'youre', 'about', 
'got', 'one', 'people', 'there', 'when', 'she', 'were', 'now', 'then', 'can', 'fucking', 
'gonna', 'shit', 'oh', 'how', 'think', 'said', 'yeah', 'had', 'fuck', 'want', 'man', 
'here', 'say', 'as', 'an', 'her', 'going', 'some', 'time', 'because', 'them', 'would', 
'see', 'hes', 'his', 'him', 'cause', 'good', 'theyre', 'did', 'from', 'why', 'well', 
'look', 'or', 'theres', 'back', 'really', 'little', 'come', 'cant', 'thing', 'who', 
'down', 'never', 'guy', 'off', 'love', 'didnt', 'okay', 'been', 'ive', 'even', 'where', 
'make', 'over', 'very', 'way', 'tell', 'ill', 'guys', 'ever', 'by', 'their', 'day', 
'into', 'take', 'could', 'put', 'two', 'something', 'went', 'hey', 'goes', 'mean', 
'these', 'other', 'more', 'will', 'shes', 'first', 'doing', 'every', 'god', 'life', 
'too', 'has', 'us', 'lot', 'always', 'give', 'much', 'uh', 'around', 'thank', 'show', 
'old', 'years', 'our', 'need', 'only', 'whats', 'big', 'kids', 'those', 'things', 
'should', 'thought', 'any', 'white', 'women', 'feel', 'let', 'am', 'black', 'gotta', 
'which', 'doesnt', 'kind', 'great', 'than', 'being', 'lets', 'yes', 'woman', 'id', 
'before', 'house', 'still', 'home', 'wanna', 'work', 'new', 'talk', 'getting', 
'trying', 'ass', 'baby', 'bit', 'night', 'talking', 'does', 'dick', 'bad', 'dad', 
'year', 'through', 'same', 'anything', 'three', 'youve', 'girl', 'real', 'after', 
'world', 'looking', 'better', 'aint', 'maybe', 'saying', 'room', 'away', 'came', 
'car', 'remember', 'next', 'nothing', 'made', 'call', 'whole', 'last', 'hear', 
'face', 'done', 'walk', 'kid', 'men', 'everybody', 'says', 'joke', 'coming', 'start', 
'used', 'name', 'most', 'friends', 'sex', 'long', 'person', 'stuff', 'another', 'sorry', 'stop']

class Database:

    def __init__(self, app):
        self.app = app
        self.engine = create_engine(self.app.config['SQLALCHEMY_DATABASE_URI'])

    def connect(self):
        Session = scoped_session(sessionmaker(bind=self.engine))
        self.session = Session()
    
    def disconnect(self):
        self.session.close()

    def getCom(self, name):
        u = self.session.query(Com).filter(Com.name == name).all()
        if u:
            return u[0]
        else:
            return u

    def getNames(self):
        names = [c.name for c in self.session.query(Com).all()]
        names.sort()
        return names

    def searchComs(self, fname, lname, key, order):
        hits = self.session.query(Com).all()
        if fname:
            hits = [h for h in hits if fname.strip().lower() in h.name.split(' ')[0]]
        if lname:
            hits = [h for h in hits if lname.strip().lower() in h.name.split(' ')[-1]]

        sorts = {'alpha':lambda x: x.name,
            'age':lambda x: 2020-int(x.yob),
            'words':lambda x: x.words,
            'uwords':lambda x: x.uwords,
            'runtime':lambda x: x.runtime,
            'wpm':lambda x: x.wpm,
            'rating': lambda x: x.rating,
            'numspec':lambda x: len(x.specials)}
        
        rev = False
        if order == 'desc':
            rev = True
        try:
            hits.sort(key = sorts[key], reverse=rev)
        except IndexError:
            print('Invalid type of sort!')
        
        #more fields
        for h in hits:
            h.id = h.name.replace(' ','_')
            h.stats = [h.name.title(), 2020-int(h.yob), h.gen, h.race, h.words,
                h.uwords, h.runtime, round(h.wpm), round(h.rating,2)]
            h.display_specials = [string.capwords(s) for s in h.specials]
        return hits
    
    def makeWordCloud(self, name, threshold):
        com = self.getCom(name)
        freq_list = []
        for i in range(len(com.top_words)):
            freq_list.append([com.top_words[i],com.top_counts[i]])
        filtered = [pair for pair in freq_list if pair[0] not in STOP_WORDS[:threshold]]
        filtered.sort(key = lambda x: x[1], reverse=True)
        top = filtered[:50]
        freq_dict = {}
        for t in top:
            freq_dict[t[0]] = t[1]
        return freq_dict

    def getTrends(self, words):
        words = [w.strip() for w in words.split(',')]
        results = {}
        rejects = []
        for w in words:
            if w:
                trend = self.session.query(Trend).filter(Trend.word == w).all()
                if trend:
                    results[w] = trend[0].toDict()
                else:
                    rejects.append(w)
        return results, rejects