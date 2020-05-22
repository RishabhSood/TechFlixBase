from flask import (
    Blueprint, render_template, request, redirect, session, url_for
)
from .decorators import login_required

import flask_pymongo

bp = Blueprint('story', __name__)


@bp.route('/storysection', methods=['GET', 'POST'])
@login_required
def story():
    if request.method == 'POST':
        return redirect(url_for('story.question'))

    from .database import storyline, users

    story_ = storyline.find_one({'id': session['user']['story_id']})
    story_text = story_['text']

    if story_.get('end', False):
        user_ = session['user']
        user_['score'] += story_['points']
        user_['end'] = True
        session['user'] = user_
        print(session)

        users.update_one({'username': session['user']['username']},
                         {'$set': {
                             'score': session['user']['score'],
                             'end': session['user']['end']
                         }})
    return render_template('story.html', story_text=story_text)


@bp.route('/question', methods=['GET', 'POST'])
@login_required
def question():
    # Managing access
    if session['user']['answered']:
        return redirect(url_for('story.options'))

    from .database import question_bank

    question_ = question_bank.find_one({'story_id': session['user']['story_id']})

    if request.method == 'POST':
        from .database import users

        answer = request.form['answer']
        if answer == question_['answer']:
            # Updating score
            session['user']['score'] += question_bank.find_one({'story_id': session['user']['story_id']})['points']

            # Updating answered status
            user = session['user']
            user['answered'] = True
            session['user'] = user

            # Updating database
            users.update_one({'username': session['user']['username']},
                             {'$set': {
                                 'score': session['user']['score'],
                                 'answered': session['user']['answered']
                             }})

            return redirect(url_for('story.options'))

    return render_template('question.html', question_text=question_['text'], alert="Wrong Answer!")


@bp.route('/options', methods=['GET', 'POST'])
@login_required
def options():
    # Managing access
    if not session['user']['answered']:
        return redirect(url_for('story.story'))

    if request.method == 'POST':
        from .database import question_bank, users

        option = request.form['options']

        if option == 'option_1':
            user_ = session['user']
            user_['story_id'] = session['options']['option_1']['story_id']
            session['user'] = user_
        elif option == 'option_2':
            user_ = session['user']
            user_['story_id'] = session['options']['option_2']['story_id']
            session['user'] = user_
        else:
            # TODO: Make a proper error page here
            return "Meanie, don't mess with my options"

        # Updating answered status in session
        session['user']['answered'] = False

        # Updating answered status and story_id in databse
        users.update_one({'username': session['user']['username']},
                         {"$set": {
                             "answered": session['user']['answered'],
                             'story_id': session['user']['story_id'],
                         }})

        return redirect(url_for('story.story'))

    from .database import optionline

    # TODO: Update options when question is answered/session starts(on the basis of answered)
    # Update the options page
    options_ = optionline.find_one({'story_id': session['user']['story_id']})
    session['options'] = {key: value for key, value in options_.items() if key not in ('_id',)}

    return render_template('options.html')


@bp.route('/leaderboard')
@login_required
def leaderboard():
    from .database import users
    leaderboard_ = users.find().sort([("score", flask_pymongo.DESCENDING), ("time", flask_pymongo.ASCENDING)])
    usernames = []
    scores = []
    ranks = []
    for rank, user in enumerate(leaderboard_, start=1):
        if user['username'] == session['user']['username']:
            user_rank = rank
        usernames.append(user['username'])
        scores.append(user['score'])
        ranks.append(rank)

    return render_template(
        "leaderboard.html",
        users=usernames,
        scores=scores,
        ranks=ranks,
        user_rank=user_rank,
    )


@bp.route('/end')
@login_required
def end():
    if session['user']['end']:
        return render_template('timer.html')

    return redirect(url_for('story.story'))
