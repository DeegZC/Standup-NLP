'''
CREATE TABLE coms(
name text, 
yob text, 
gen text, 
race text, 
specials text[], 
words int,
uwords int,
runtime int,
wpm real,
uwpm real,
rating real,
top_words text[])
'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, ARRAY, REAL

Base = declarative_base()

class Com(Base):
    __tablename__ = 'coms'
    name = Column(Text, primary_key=True)
    yob = Column(Text) 
    gen = Column(Text) 
    race = Column(Text)
    specials = Column(ARRAY(Text)) 
    words = Column(Integer)
    uwords = Column(Integer)
    runtime = Column(Integer)
    wpm = Column(REAL)
    uwpm = Column(REAL)
    rating = Column(REAL)
    top_words = Column(ARRAY(Text))
    top_counts = Column(ARRAY(Integer))

    def __str__(self):
        display = '''\
Name:     ''' + self.name.title()+'''\n\
YOB:      {self.yob}\n\
Gender:   {self.gen}\n\
Race:     {self.race}\n\
Specials:'''.format(self=self)
        for s in self.specials:
            display+='\n- '+s.title()
        supp =  '\nTotal Words:         '+str(self.words)+\
                '\nTotal Unique Words:  '+str(self.uwords)+\
                '\nTotal Runtime:       '+str(self.runtime)+\
                '\nWords/Minute         '+str(self.wpm)+\
                '\nUnique Words/Minute  '+str(self.uwpm)+\
                '\nAverage Rating       '+str(self.rating)
        return display+supp