import os
from sqlalchemy import Column, String, Integer, create_engine, Date
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
    __tablename__ = "user"
    id = Column(Integer,primary_key = True)
    hash = Column(String, nullable = False, unique = True)
    salt = Column(String, nullable = False)
    name = Column(String, nullable = False)

class Qtable(db.Model):
    __tablename__ = "qtable"
    id = Column(Integer, primary_key = True)
    date = Column(Date, nullable = False)
    q1 = Column(String)
    q2 = Column(String)
    q3 = Column(String)

