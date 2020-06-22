import os
from sqlalchemy import Column, String, Integer, create_engine, Date, Boolean
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "covid"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)
db = SQLAlchemy()


def drop_create_all():
    db.drop_all()
    db.create_all()


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



class Qtable(db.Model):
    __tablename__ = "qtable"
    id = Column(Integer, primary_key = True)
    date = Column(Date, nullable = False)
    userid = Column(Integer)
    username = Column(String)
    q1 = Column(Boolean)
    q2 = Column(Boolean)
    q3 = Column(Boolean)

    def __init__(self, date, userid, username, q1, q2, q3):
        self.date = date
        self.userid = userid
        self.username = username
        self.q1 = q1
        self.q2 = q2
        self.s3 = q3
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

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
