# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 07:22:21 2020

@author: soodr
"""


from flask import Flask, render_template, request, redirect, url_for, session
from flask_mongoalchemy import MongoAlchemy
import hashlib

app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'TECHFLIX'
mongo = MongoAlchemy(app)

class Login(mongo.Document):
    username = mongo.StringField()
    password = mongo.StringField()
    
class Storyline(mongo.Document):
    s_id = mongo.StringField()
    s_content = mongo.StringField()
    q_id = mongo.StringField()
    
class Questions(mongo.Document):
    q_id = mongo.StringField()
    question = mongo.StringField()
    answer = mongo.StringField()
    op_id = mongo.StringField()
    points = mongo.IntField()

class Options(mongo.Document):
    op_id = mongo.StringField()
    opt_1 = mongo.StringField()
    opt_2 = mongo.StringField()
    s_id_1 = mongo.StringField()
    s_id_2 = mongo.StringField()
    
st = Storyline.query.filter(Storyline.s_id == '1').first()
qn = Questions.query.filter(Questions.q_id == '0').first()
    
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('display_story'))
    
    return render_template('home.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        existing_user = Login.query.filter(Login.username == request.form['username']).first()
        if existing_user is not None:
            hash = hashlib.sha256(request.form['password'].encode()).hexdigest()
            if existing_user.password == hash:
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            else:
                return render_template('signin.html', alert = 'Invalid Username/Password')
            
        return render_template('signin.html', alert = 'Invalid Username/Password')
    
    return render_template('signin.html', alert = '')

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        existing_user = Login.query.filter(Login.username == request.form['username']).first()
        if existing_user is None:
            if request.form['password'] == request.form['confirm-password']:
                uname = request.form['username']
                hashpass = hashlib.sha256(request.form['password'].encode()).hexdigest()
                new_user = Login(username = uname, password = hashpass)
                new_user.save()
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            else:
                return render_template('signup.html', alert = 'Passwords don\'t match!')
        
        return render_template('signup.html', alert = 'That username already exists!')
    
    return render_template('signup.html', alert = '')

@app.route('/storysection', methods=['GET', 'POST'])
def display_story():
    global qn
    story_sect = st.s_content
    qn = Questions.query.filter(Questions.q_id == st.q_id).first()
    if request.method == 'POST':
        return redirect(url_for('display_question'))
    return render_template('index.html', story_section = story_sect)

@app.route('/question', methods=['GET', 'POST'])
def display_question():
    my_question = qn.question
    if request.method == 'POST':
        age = request.form['age']
        if age == qn.answer:
            return redirect(url_for('display_option'))
    return render_template('question.html', question = my_question)

@app.route('/option', methods=['GET', 'POST'])
def display_option():
    global qn
    if request.method == 'POST':
        option = request.form['options']
        if option == 'option2':
            #qn = Questions.query.filter(Questions.qid == '2').first()
            return redirect(url_for('display_story'))
    return render_template('options.html', options = "pehla prasnhna ye rha aapki screen par")

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run()
