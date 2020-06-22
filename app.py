import os
from flask import Flask, request, abort, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from flask_migrate import Migrate
from models import setup_db, User, Qtable, Questions, drop_create_all
import bcrypt


app = Flask(__name__)
setup_db(app)
CORS(app)
questions = ["Are you experiencing any flu symptoms-like cold, cough?",
"Are you experiencing any of these conditions: Stomach upset, vomiting, fatigue?",
"Are you suffering from shortness of breath or other respiratory problems?"]


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods = ['POST'])
def login():
    passkey = bytes(request.form['password'],'utf-8')
    username = request.form['username']
    user_found = User.query.filter(User.name == username).one_or_none()

    if user_found == None:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(passkey, salt)
        new_user = User(hashed.decode('utf-8'), username, salt)
        new_user.insert()
        return redirect(url_for('questionnaire', name = username, user_id = new_user.id))
    if bcrypt.checkpw(passkey, user_found.hash_key.encode('utf-8')) :
        return redirect(url_for('questionnaire', name = username, user_id = user_found.id))
    else:
        print("false password")
        return "Enter correct Password"
    

@app.route('/questionnaire')
def questionnaire():
    name = request.args['name']
    user_id = request.args['user_id']
    db_questions = Questions.query.all()
    return render_template("survey.html", questions = [q.format()["name"] for q in db_questions], name = name, user_id = user_id)

@app.route('/questionnaire', methods = ["POST"])
def add_question():
    data = request.get_json()
    question = Questions(name=data['name'])
    question.insert()
    return "Added question"

@app.route('/questionnaire_submit', methods = ["POST"])
def store_questionnaire():
    print(request.form)
    return "Submitted"
