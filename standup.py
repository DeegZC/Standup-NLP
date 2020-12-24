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
#-----------------------------------------------------------------------
# cloudinary.config()

#-----------------------------------------------------------------------
import os
from flask import send_from_directory
app = Flask(__name__, template_folder='.')
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
plt.style.use('fivethirtyeight')

db = Database(app)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
#-----------------------------------------------------------------------

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
    db.connect()
    words, rejects = db.getTrends(request.form.get('words'))
    db.disconnect()
    fig = Figure()
    axis = fig.add_subplot(1,1,1)
    for w in words:
        x = [year for year in list(w.keys()) if w[year]]
        y = [w[year] for year in x]
        axis.plot(x,y)
        axis.legend(words)
    return make_response(render_template('trends_plot.html',
        image = encodeFig(fig),
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