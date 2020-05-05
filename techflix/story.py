from flask import (
    Blueprint, render_template, request, redirect, g, session, url_for
)
from .auth import login_required

bp = Blueprint('story', __name__)


@bp.route('/storysection', methods=['GET', 'POST'])
@login_required
def story():
    from .database import storyline

    story_text = storyline.find_one({'id': session['user']['story_id']})['text']
    if request.method == 'POST':
        return redirect(url_for('story.question'))

    return render_template('story.html', story_text=story_text)


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
            # TODO: Make this better as it is currently lost on logout
            options_ = optionline.find_one({'story_id': session['user']['story_id']})
            session['options'] = {key: value for key, value in options_.items() if key not in ('_id',)}
            print(session['options'])
            # user = users.find_one({'username': session['user']['username']})

            users.update_one({'username': session['user']['username']}, {"$set": {"score": session['user']['score']}})
            return redirect(url_for('story.options'))

    return render_template('question.html', question_text=question_['text'])


@bp.route('/options', methods=['GET', 'POST'])
@login_required
def options():
    if request.method == 'POST':
        from .database import question_bank

        option = request.form['options']

        if option == 'option_1':
            user_ = session['user']
            user_['story_id'] = session['options']['option_1']['story_id']
            session['user'] = user_
            print('yo')
        elif option == 'option_2':
            user_ = session['user']
            user_['story_id'] = session['options']['option_2']['story_id']
            session['user'] = user_
        else:
            # TODO: Make a proper error page here
            return "Meanie, don't mess with my options"

        session['user']['score'] += question_bank.find_one({'story_id': session['user']['story_id']})['points']
        return redirect(url_for('story.story'))

    return render_template('options.html')


@bp.route('/leaderboard')
@login_required
def leaderboard():
    from .database import leaderboard
    usernames = []
    scores = []
    ranks = []
    for rank, user in enumerate(leaderboard, start=1):
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
        user_rank = user_rank,
    )
