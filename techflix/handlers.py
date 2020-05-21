# Handles the working of the entire application

from flask import (
    Blueprint, redirect, url_for, session, request
)

bp = Blueprint('handlers', __name__)

# Constants
EXEMPT_ENDPOINTS = ('story.leaderboard', 'auth.logout', 'story.end')


@bp.before_app_request
def ending():
    user = session.get('user')

    if user:
        if session['user']['end'] and (request.endpoint not in EXEMPT_ENDPOINTS) and ('static' not in request.endpoint):
            return redirect(url_for('story.end'))
