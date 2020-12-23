#!/usr/bin/env python

#-----------------------------------------------------------------------
# app.py
#-----------------------------------------------------------------------

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
#-----------------------------------------------------------------------
# cloudinary.config()

#-----------------------------------------------------------------------
import os
from flask import send_from_directory
app = Flask(__name__, template_folder='.')
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


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

@app.route('/makeWordCloud', methods=['GET','POST'])
def makeWordCloud():
    db.connect()
    validArgs = True
    words = []
    try:
        words = db.makeWordCloud(request.form.get('name'), int(request.form.get('threshold')))
    except Exception:
        validArgs = False

    wc = WordCloud(background_color="white", colormap="Dark2",
               max_font_size=150, random_state=42)
    wc.generate_from_frequencies(words)
    fig = Figure()
    axis = fig.add_subplot(1,1,1)
    axis.imshow(wc, interpolation="bilinear")
    axis.axis('off')
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    
    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')

    html = render_template('show_word_cloud.html',
        validArgs = validArgs,
        image=pngImageB64String)
    db.disconnect()
    return make_response(html)