from flask import (
    Blueprint, render_template, request, redirect, g, session, url_for
)
from .auth import login_required

bp = Blueprint('story', __name__)


@bp.route('/storysection', methods=['GET', 'POST'])
@login_required
def story():
    from .database import storyline

    story_ = storyline.find_one({'id': session['user']['story_id']})
    if request.method == 'POST':
        return redirect(url_for('story.question'))

    return render_template('story.html', story_text=story_['text'])


@bp.route('/question', methods=['GET', 'POST'])
@login_required
def question():
    from .database import question_bank

    question_ = question_bank.find_one({'story_id': session['user']['story_id']})
    if request.method == 'POST':
        from .database import users, optionline

        answer = request.form['answer']
        if answer == question_['answer']:
            # Update the options page
            # TODO: Make this better as it i currently lost on logout
            session['options'] = optionline.find_one({'story_id': session['user']['story_id']})
            print(session['user']['username'])
            users.update_one({'username': 'test'}, {"$set": {"score": session['user']['score']}})
            return redirect(url_for('story.options'))

    return render_template('question.html', question_text=question_['text'])


@bp.route('/options', methods=['GET', 'POST'])
def options():
    if request.method == 'POST':
        from .database import question_bank

        option = request.form['options']

        if option == 'option1':
            session['user']['story_id'] = session['options']['option_1']['story_id']
        elif option == 'option2':
            session['user']['story_id'] = session['options']['option_2']['story_id']
        else:
            # TODO: Make a proper error page here
            return "Meanie, don't mess with my options"

        session['user']['score'] += question_bank.find_one({'story_id': session['user']['story_id']})['points']
        return redirect(url_for('story.story'))

    return render_template('options.html')
