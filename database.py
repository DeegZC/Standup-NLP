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
        return [c.name.title() for c in self.session.query(Com).all()]

    def getComByName(self, fname, lname):
        hits = self.session.query(Com).all()
        if fname:
            hits = [h for h in hits if fname.lower() in h.name.split(' ')[0]]
        if lname:
            hits = [h for h in hits if lname.lower() in h.name.split(' ')[-1]]
        return hits
