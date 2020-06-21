import os
from flask import Flask
from sqlalchemy import Column, String, Integer, create_engine, Date, Boolean
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "covid"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)
app = Flask(__name__)
db = SQLAlchemy(app)


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
    q1 = Column(Boolean)
    q2 = Column(Boolean)
    q3 = Column(Boolean)

    def __init__(self, date, q1, q2, q3):
        self.date = date
        self.q1 = q1
        self.q2 = q2
        self.s3 = q3
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
