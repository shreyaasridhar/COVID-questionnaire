import os
from flask import Flask, request, abort, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS
import json
from datetime import datetime
from flask_migrate import Migrate
from models import setup_db, User, Qtable, Questions, drop_create_all
import bcrypt

def create_app():
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    app.config.from_object('config')
    
    if reset_db == True:
        drop_create_all()

    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/login', methods = ['POST'])
    def login():
        try:
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
               flash('Enter correct Password')
            return redirect(url_for('index'))
        except SQLAlchemyError as e:
            print(request.form) # can be saved to a file or a backup database
            # flash('User could not be created!')

    @app.route("/forgot")
    def forgot():
        return render_template('reset.html')

    @app.route('/reset', methods = ['POST'])
    def reset_password():
        passkey = bytes(request.form['password'],'utf-8')
        username = request.form['username']
        user_found = User.query.filter(User.name == username).one_or_none()
        if user_found == None:
            flash('Invalid user')
            return redirect(url_for('index'))
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(passkey, salt)
        user_found.salt = salt
        user_found.hash_key = hashed.decode('utf-8')
        user_found.update()
        return redirect(url_for('questionnaire', name = username, user_id = user_found.id))

    @app.route('/questionnaire')
    def questionnaire():
        name = request.args['name']
        user_id = request.args['user_id']
        success = request.args['success'] if 'success' in request.args else None
        db_questions = Questions.query.all()
        return render_template('survey.html', questions = [q.format()['name'] for q in db_questions], name = name, user_id = user_id, success=success)

    @app.route('/questionnaire', methods = ['POST'])
    def add_question():
        data = request.get_json()
        question = Questions(name=data['name'])
        question.insert()
        return 'Added question'

    @app.route('/questionnaire_submit', methods = ['POST'])
    def store_questionnaire():
        data = request.form
        entry = Qtable(data['today'], data['user_id'], data['username'], [data[str(i)] == '1' for i in range(1, len(data)-2)])
        entry.insert()
        return redirect(url_for('questionnaire', name = data['username'], user_id = data['user_id'], success=True))

    @app.route('/users_today')
    def today():
        now = datetime.now().strftime('%Y-%m-%d')
        print(now)
        today = Qtable.query.filter(Qtable.date == now).all()
        return jsonify({
            'success':True,
            'today': [t.format() for t in today],
            'total_entries': len(today)
        })

    @app.route('/date-filter')
    def filter_date():
        return render_template('filter.html', filtered=None)

    @app.route('/users-by-date', methods = ['POST'])
    def user_by_date():
        date_req = request.form['date']
        dated = Qtable.query.filter(Qtable.date == date_req).all()
        return render_template('filter.html', filtered={
            'date': date_req,
            'users': [t.format() for t in dated],
            'total_entries': len(dated)
        })
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

