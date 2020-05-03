# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:14:06 2020

@author: soodr
"""

from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
import hashlib
import datetime
import pymongo

app = Flask(__name__)
app.config["MONGO_URI"] = (
    "***REMOVED***"
)
app.config['MONGO_DBNAME'] = "TECHFLIX_DB"
mongo = PyMongo(app)
Login = mongo.db.USER_DATA
question_data = mongo.db.QUESTIONS
story_data = mongo.db.STORYLINE
option_data = mongo.db.OPTIONS
leaderboard = mongo.db.LEADERBOARD

st = story_data.find_one({'s_id': '1'})
qn = question_data.find_one({'q_id': '0'})
op = option_data.find_one({'op_id': '0'})


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('display_story'))
    
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        existing_user = Login.find_one({'username': request.form['username']})
        if existing_user is not None:
            hash = hashlib.sha256(request.form['password'].encode()).hexdigest()
            if existing_user['password'] == hash:
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            else:
                return render_template('signin.html', alert='Invalid Username/Password')
            
        return render_template('signin.html', alert='Invalid Username/Password')
    
    return render_template('signin.html', alert='')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        existing_user = Login.find_one({'username': request.form['username']})
        if existing_user is None:
            if request.form['password'] == request.form['confirm-password']:
                uname = request.form['username']
                hashpass = hashlib.sha256(request.form['password'].encode()).hexdigest()
                Login.insert_one({'email': request.form['email'],
                                  'username': uname,
                                  'password': hashpass,
                                  'score': 0,
                                  'time': datetime.datetime.utcnow(),
                                  's_id': '1'})
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            else:
                return render_template('signup.html', alert='Passwords don\'t match!')
        
        return render_template('signup.html', alert='That username already exists!')
    
    return render_template('signup.html', alert='')


@app.route('/storysection', methods=['GET', 'POST'])
def display_story():
    global qn
    global st
    user = Login.find_one({'username': session['username']})
    st = story_data.find_one({'s_id': user['s_id']})
    score = user['score']
    story_sect = st['s_content']
    qn = question_data.find_one({'q_id': st['q_id']})
    if request.method == 'POST':
        return redirect(url_for('display_question'))
    return render_template('index.html', story_section=story_sect, username=session['username'], score=score)


@app.route('/question', methods=['GET', 'POST'])
def display_question():
    global op
    my_question = qn['question']
    user = Login.find_one({'username': session['username']})
    score = user['score']
    op = option_data.find_one({'op_id': qn['op_id']})
    if request.method == 'POST':
        answer = request.form['answer']
        if answer == qn['answer']:
            user = Login.find_one({'username': session['username']})
            Login.update_one(user, {"$set": {"time": datetime.datetime.utcnow()}})
            return redirect(url_for('display_option'))
    return render_template('question.html', question=my_question, username=session['username'], score=score)


@app.route('/option', methods=['GET', 'POST'])
def display_option():
    global qn
    global st
    user = Login.find_one({'username': session['username']})
    score = user['score']
    
    if request.method == 'POST':
        option = request.form['options']
        if option == 'option1':
            qn = question_data.find_one({'q_id': op['q_id']})
            st = story_data.find_one({'s_id': op['s_id_1']})
            score += qn['points']
            Login.update_one(user, {"$set": {"score": score, "s_id": op['s_id_1']}})
            return redirect(url_for('display_story'))
        if option == 'option2':
            qn = question_data.find_one({'q_id': op['q_id']})
            st = story_data.find_one({'s_id': op['s_id_2']})
            score += qn['points']
            Login.update_one(user, {"$set": {"score": score, "s_id": op['s_id_2']}})
            return redirect(url_for('display_story'))
    return render_template('options.html', option_text=op['option_text'], option1=op['opt_1'], option2=op['opt_2'],
                           username=session['username'], score=score)


@app.route('/leaderboard')
def leaderboard():
    leaderbd = Login.find().sort([("score", pymongo.DESCENDING), ("time", pymongo.ASCENDING)])
    users_list = []
    scores_list = []
    rank_list = []
    rank = 1
    for x in leaderbd:
        global user_rank
        if x['username'] == session['username']:
            user_rank = rank
        users_list += [x['username']]
        scores_list += [x['score']]
        rank_list += [rank]
        rank += 1
    user = session['username']
    return render_template("leaderboard.html", users=users_list, scores=scores_list,
                           ranks=rank_list, truser=user, userrank=user_rank)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run()
