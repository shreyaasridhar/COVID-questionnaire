import os
from sqlalchemy import Column, String, Integer, create_engine, Date, Boolean
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "covid"
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)
database_path = "postgres://dkluuncfcsvasb:d7b7c37214917c1895b06adf3e73f2f57575f1935b105e3390d4744c5190392a@ec2-52-0-155-79.compute-1.amazonaws.com:5432/ddn59k3b73e2f8"
db = SQLAlchemy()
questions = ["Are you experiencing any flu symptoms-like cold, cough?",
"Are you experiencing any of these conditions: Stomach upset, vomiting, fatigue?",
"Are you suffering from shortness of breath or other respiratory problems?"]

def drop_create_all():
    db.drop_all()
    db.create_all()

    for i in questions:
        question = Questions(i)
        question.insert()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer,primary_key = True)
    hash_key = Column(String, nullable = False, unique = True)
    salt = Column(String, nullable = False)
    name = Column(String, nullable = False)

    def __init__(self, hash_key, name, salt):
        self.hash_key = hash_key
        self.name = name
        self.salt = salt
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

class Qtable(db.Model):
    __tablename__ = "qtable"
    id = Column(Integer, primary_key = True)
    date = Column(Date, nullable = False)
    userid = Column(Integer)
    username = Column(String)
    questions = Column(db.ARRAY(String))

    def __init__(self, date, userid, username, questions):
        self.date = date
        self.userid = userid
        self.username = username
        self.questions = questions
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            "Username":self.username,
            "Userid":self.userid,
            "questions":self.questions
        }

class Questions(db.Model):
    __tablename__ = "questions"
    id = Column(Integer, primary_key = True)
    name = Column(String)

    def __init__(self, name):
        self.name = name
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            "name" : self.name
        }
