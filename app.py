import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from models import setup_db, User, Qtable, drop_create_all


app = Flask(__name__)
setup_db(app)
CORS(app)


@app.route('/')
def index():
    return "Hello From Server"
