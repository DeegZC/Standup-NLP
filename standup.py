#!/usr/bin/env python

#-----------------------------------------------------------------------
# app.py
#-----------------------------------------------------------------------

from numpy.core.getlimits import MachArLike
from database import Database
from flask import Flask, request, make_response, redirect, url_for, render_template, session
from config import Config
import numpy as np
import io
import base64
import time
from wordcloud import WordCloud
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
#-----------------------------------------------------------------------
# cloudinary.config()
WPY = {1965: 11563,
 1971: 5032,
 1977: 10099,
 1978: 10683,
 1979: 9442,
 1982: 8767,
 1983: 25302,
 1984: 7595,
 1986: 10099,
 1987: 13565,
 1988: 6722,
 1990: 7704,
 1991: 9936,
 1992: 11414,
 1993: 16362,
 1994: 11351,
 1996: 15557,
 1997: 11319,
 1998: 18274,
 1999: 39262,
 2000: 14378,
 2001: 7795,
 2002: 11031,
 2003: 3253,
 2004: 37441,
 2005: 17086,
 2006: 47256,
 2007: 59758,
 2008: 36219,
 2009: 55173,
 2010: 104077,
 2011: 72382,
 2012: 103717,
 2013: 132075,
 2014: 106381,
 2015: 149635,
 2016: 220546,
 2017: 337007,
 2018: 311841,
 2019: 268951,
 2020: 157435}
#-----------------------------------------------------------------------
import os
from flask import send_from_directory
app = Flask(__name__, template_folder='.')
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
plt.style.use('fivethirtyeight')

db = Database(app)

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
@app.route('/index', methods=['GET'])
def home():
    if request.args.get('warned'):
        session['warned']=True
        print('found warned')
    if 'warned' not in session:
        return redirect('warning')
    print('passed tests. now rendering')
    return make_response(render_template('index.html'))
    
#-----------------------------------------------------------------------
@app.route('/warning', methods=['GET'])
def warning():
    return make_response(render_template('warning.html'))
    
#-----------------------------------------------------------------------
@app.route('/comicSearch', methods=['GET','POST'])
def comicSearch():
    if 'warned' not in session:
        return redirect('warning')
    return make_response(render_template('com_search.html'))

#-----------------------------------------------------------------------

@app.route('/comicSearchResults', methods=['POST','GET'])
def comicSearchResults():
    t0 = time.perf_counter()
    db.connect()
    print('getting coms')
    comics = db.searchComs(request.form.get('fname'),request.form.get('lname'), request.form.get('key'),request.form.get('order'))
    html = render_template('com_search_results.html',
        comics = comics,
        results = len(comics),
        time = round(time.perf_counter()-t0,2))
    response = make_response(html)
    db.disconnect()
    return response

@app.route('/about', methods=['GET'])
def about():
    return make_response(render_template('about.html'))

@app.route('/wordClouds', methods=['GET'])
def wordClouds():
    if 'warned' not in session:
        return redirect('warning')
    db.connect()
    html = render_template('word_clouds.html',
        names=db.getNames(),
        default_threshold=200)
    db.disconnect()
    return make_response(html)

@app.route('/pca', methods=['GET','POST'])
def pca():
    return make_response(render_template('pca.html'))

@app.route('/trends', methods=['GET','POST'])
def trends():
    return make_response(render_template('trends.html'))

@app.route('/plotTrends', methods=['GET','POST'])
def plotTrends():
    validYears = True
    word_error = ''
    rejects = []
    fig = 0
    try:
        lower = int(request.form.get('lower'))
        upper = int(request.form.get('upper'))
        if lower > upper or lower > 2020 or lower < 1965 or upper > 2020 or lower < 1965:
            raise Exception
        db.connect()
        words, rejects = db.getTrends(request.form.get('words'))
        if not words:
            word_error = 'No words found in the input area.'
        db.disconnect()
        fig = Figure()
        axis = fig.add_subplot(1,1,1)
        for data in words.values():
            x = [year for year in list(data.keys()) if data[year] and year >= lower and year <= upper]
            y = [100*data[year] for year in x]
            for year in x:
                axis.annotate(round(WPY[year]*data[year]), (year, 100*data[year]))
            axis.plot(x,y)
        axis.legend(list(words.keys()))
        axis.set_xlabel('Year')
        axis.axis('on')
        axis.set_ylabel('Percentage of Words that Year')
        fig = encodeFig(fig)
    except Exception:
        validYears = False

    return make_response(render_template('trends_plot.html',
        image = fig,
        validYears = validYears,
        err=word_error,
        rejects = rejects))

@app.route('/makeWordCloud', methods=['GET','POST'])
def makeWordCloud():
    db.connect()
    validArgs = True
    words = []
    image = 0
    try:
        thresh = int(request.form.get('threshold'))
        if thresh > 250:
            raise Exception
        words = db.makeWordCloud(request.form.get('name'), thresh)
        wc = WordCloud(background_color="white", colormap="Dark2",
               max_font_size=150, random_state=42)
        wc.generate_from_frequencies(words)
        fig = Figure()
        axis = fig.add_subplot(1,1,1)
        axis.imshow(wc, interpolation="bilinear")
        axis.axis('off')
        image = encodeFig(fig)
    except Exception:
        validArgs = False

    html = render_template('show_word_cloud.html',
        validArgs = validArgs,
        image= image)
    db.disconnect()
    return make_response(html)

def encodeFig(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String