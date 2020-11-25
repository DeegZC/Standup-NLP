#!/usr/bin/env python

#-----------------------------------------------------------------------
# app.py
#-----------------------------------------------------------------------

from database import Database
from flask import Flask, request, make_response, redirect, url_for, render_template, session
from config import Config
import numpy as np
import time
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
    if 'warned' in request.args:
        session['warned']=True
        print('found warned')
    if 'warned' not in session:
        redirect('warning')
        print('redirecting')
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
        redirect('warning')

    return make_response(render_template('com_search.html'))

#-----------------------------------------------------------------------

@app.route('/comicSearchResults', methods=['POST','GET'])
def comicSearchResults():
    t0 = time.perf_counter()
    if 'warned' not in session:
        redirect('warning')
    db.connect()
    comics = db.getComByName(request.args['fname'],request.args['lname'])

    html = render_template('com_search_results.html',
        comics = comics,
        results = len(comics),
        time = round(time.perf_counter()-t0,2))
    response = make_response(html)
    db.disconnect()
    return response
#-----------------------------------------------------------------------
