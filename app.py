# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 07:21:58 2020

@author: soodr
"""


from flask import Flask, render_template, request, redirect, url_for
from flask_mongoalchemy import MongoAlchemy

app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'TECHFLIX'
db = MongoAlchemy(app)

class Storyline(db.Document):
    s_id = db.StringField()
    s_content = db.StringField()
    q_id = db.StringField()
    
class Questions(db.Document):
    q_id = db.StringField()
    question = db.StringField()
    answer = db.StringField()
    op_id = db.StringField()
    points = db.IntField()

class Options(db.Document):
    op_id = db.StringField()
    opt_1 = db.StringField()
    opt_2 = db.StringField()
    s_id_1 = db.StringField()
    s_id_2 = db.StringField()
    
st = Storyline.query.filter(Storyline.s_id == '1').first()
qn = Questions.query.filter(Questions.q_id == '0').first()
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
            qn = Questions.query.filter(Questions.qid == '2').first()
            return redirect(url_for('display_story'))
    return render_template('options.html', options = "pehla prasnhna ye rha aapki screen par")

if __name__ == "__main__":
    app.run()