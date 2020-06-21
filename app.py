import os
from flask import Flask, request, abort, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from flask_migrate import Migrate
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
    passkey = bytes(request.form['password'],'utf-8')
    username = request.form['username']
    user_found = User.query.filter(User.name == username).one_or_none()

    if user_found == None:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(passkey, salt)
        new_user = User(hashed.decode('utf-8'), username, salt)
        new_user.insert()
        return redirect(url_for('questionnaire'))
    if bcrypt.checkpw(passkey, user_found.hash_key.encode('utf-8')) :
        return redirect(url_for('questionnaire'))
    else:
        print("false password")
        return "Enter correct Password"
    

@app.route('/questionnaire')
def questionnaire():
    return render_template("survey.html")
