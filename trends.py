from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Text, REAL

Base = declarative_base()

class Trend(Base):
    __tablename__ = 'trends'
    word = Column(Text, primary_key=True)
    y1965 = Column(REAL)
    y1971 = Column(REAL)
    y1977 = Column(REAL)
    y1978 = Column(REAL)
    y1979 = Column(REAL)
    y1982 = Column(REAL)
    y1983 = Column(REAL)
    y1984 = Column(REAL)
    y1986 = Column(REAL)
    y1987 = Column(REAL)
    y1988 = Column(REAL)
    y1990 = Column(REAL)
    y1991 = Column(REAL)
    y1992 = Column(REAL)
    y1993 = Column(REAL)
    y1994 = Column(REAL)
    y1996 = Column(REAL)
    y1997 = Column(REAL)
    y1998 = Column(REAL)
    y1999 = Column(REAL)
    y2000 = Column(REAL)
    y2001 = Column(REAL)
    y2002 = Column(REAL)
    y2003 = Column(REAL)
    y2004 = Column(REAL)
    y2005 = Column(REAL)
    y2006 = Column(REAL)
    y2007 = Column(REAL)
    y2008 = Column(REAL)
    y2009 = Column(REAL)
    y2010 = Column(REAL)
    y2011 = Column(REAL)
    y2012 = Column(REAL)
    y2013 = Column(REAL)
    y2014 = Column(REAL)
    y2015 = Column(REAL)
    y2016 = Column(REAL)
    y2017 = Column(REAL)
    y2018 = Column(REAL)
    y2019 = Column(REAL)
    y2020 = Column(REAL)

    def toDict(self):
        return {1965: self.y1965, 1971: self.y1971, 1977: self.y1977, 1978: self.y1978, 1979: self.y1979, 
        1982: self.y1982, 1983: self.y1983, 1984: self.y1984, 1986: self.y1986, 1987: self.y1987, 1988: self.y1988,
        1990: self.y1990, 1991: self.y1991, 1992: self.y1992, 1993: self.y1993, 1994: self.y1994, 1996: self.y1996, 
        1997: self.y1997, 1998: self.y1998, 1999: self.y1999, 2000: self.y2000, 2001: self.y2001, 2002: self.y2002, 
        2003: self.y2003, 2004: self.y2004, 2005: self.y2005, 2006: self.y2006, 2007: self.y2007, 2008: self.y2008, 
        2009: self.y2009, 2010: self.y2010, 2011: self.y2011, 2012: self.y2012, 2013: self.y2013, 2014: self.y2014, 
        2015: self.y2015, 2016: self.y2016, 2017: self.y2017, 2018: self.y2018, 2019: self.y2019, 2020: self.y2020}