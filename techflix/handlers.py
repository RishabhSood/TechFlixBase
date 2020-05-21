# Handles the working of the entire application

from flask import (
    Blueprint, redirect, url_for, session
)

bp = Blueprint('handlers', __name__)


@bp.before_app_request
def ending():
    user = session.get('user')
    print("In ending")
    print(dict(session))

    if user:
        if session['user']['end']:
            print("Tried to end?")
            return redirect(url_for('story.leaderboard'))
