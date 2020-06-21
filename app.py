import os
from flask import Flask, request, abort, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from models import setup_db, User, Qtable, drop_create_all
import bcrypt


app = Flask(__name__)
setup_db(app)
CORS(app)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login',methods = ['POST'])
def login():
    print(request.form)
    return redirect(url_for('questionnaire'))

@app.route('/questionnaire')
def questionnaire():
    return "QUESTIOINNAIR"
