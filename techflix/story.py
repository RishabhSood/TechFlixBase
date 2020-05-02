from flask import (
    Blueprint, render_template, request, redirect, g, session, url_for
)

bp = Blueprint('story', __name__)


@bp.route('/storysection', methods=['GET', 'POST'])
def story():
    from .database import users, stories

    user = users.find_one({'username': session['username']})
    score = user['score']
    # story_sect = st['s_content']
    if request.method == 'POST':
        return redirect(url_for('story.question'))
    return render_template('story.html',
                           # story_section=story_sect,
                           username=session['username'],
                           score=score)


@bp.route('/question', methods=['GET', 'POST'])
def question():
    from .database import users

    # my_question = qn['question']
    user = users.find_one({'username': session['username']})
    score = user['score']
    if request.method == 'POST':
        answer = request.form['answer']
        # if answer == qn['answer']:
        #     score += qn['points']
        #     user = users.find_one({'username': session['username']})
        #     users.update_one(user, { "$set": { "score": score } })
        #     return redirect(url_for('story.options'))
    return render_template('question.html',
                           # question=my_question,
                           username=session['username'],
                           score=score)


@bp.route('/options', methods=['GET', 'POST'])
def options():
    from .database import users

    user = users.find_one({'username': session['username']})
    score = user['score']
    if request.method == 'POST':
        option = request.form['options']
        if option == 'option2':
            #qn = Questions.query.filter(Questions.qid == '2').first()
            return redirect(url_for('story.story'))
    return render_template('options.html',
                           option_text="pehla prasnhna ye rha aapki screen par",
                           username=session['username'],
                           score=score)
