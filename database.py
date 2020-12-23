#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from com import Com
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

#-----------------------------------------------------------------------

DEFAULT_PROFILE_PIC = 'https://res.cloudinary.com/hvc9pv02i/image/upload/v1603764923/gjlxtya69lekqr4nw97w.jpg'
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
            hits = [h for h in hits if fname.lower() in h.name.split(' ')[0]]
        if lname:
            hits = [h for h in hits if lname.lower() in h.name.split(' ')[-1]]

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
        return hits
    
    def makeWordCloud(self, name, threshold):
        com = self.getCom(name)
        return com.top_words[:10]
