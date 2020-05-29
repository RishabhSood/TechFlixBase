# Handles the working of the entire application

from flask import (
    Blueprint, redirect, url_for, session, request, render_template
)
from .decorators import login_required
from .deployed import (
    TIME_STRING_FORMAT, JS_TIME_STRING_UTC_FORMAT
)

import datetime

bp = Blueprint('handlers', __name__)

# Endpoints
EXEMPT_ENDPOINTS = ('story.leaderboard', 'auth.logout')
END_ENDPOINT = 'handlers.end'

# The end times...
END_TIME_STRING = "2020-06-02 19:30:00+0530"

END_TIME = datetime.datetime.strptime(END_TIME_STRING, TIME_STRING_FORMAT)
END_TIME_UTC = END_TIME.astimezone(tz=datetime.timezone.utc)

JS_TIME_STRING_UTC = datetime.datetime.strftime(END_TIME_UTC, JS_TIME_STRING_UTC_FORMAT)


@bp.route('/end')
@login_required
def end():
    """Handling for this in ending()"""

    return render_template(
        'timer.html',
        TIME_STRING_UTC=JS_TIME_STRING_UTC,
    )


@bp.before_app_request
def ending():
    user = session.get('user')

    # Never need to be tested
    if not request.endpoint or request.endpoint in EXEMPT_ENDPOINTS or 'static' in request.endpoint:
        return

    # If the event ended, log the user out, redirect to leaderboard
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    if now > END_TIME:
        if user:
            return redirect(url_for('auth.logout'))
        return redirect(url_for('story.leaderboard'))

    # If user reached the end, redirect to the end
    if user and session['user']['end']:
        if request.endpoint != END_ENDPOINT:
            return redirect(url_for(END_ENDPOINT))
        return

    # If trying to access url_for('end') illegally
    if request.endpoint == END_ENDPOINT:
        print("Illegal access")
        return redirect(url_for('index'))
