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
EXEMPT_ENDPOINTS = ('story.leaderboard', 'auth.logout', 'handlers.end')
END_ENDPOINT = 'handlers.end'

# The end times...
END_TIME_STRING = "2020-06-02 00:00:00+0530"

END_TIME = datetime.datetime.strptime(END_TIME_STRING, TIME_STRING_FORMAT)
END_TIME_UTC = END_TIME.astimezone(tz=datetime.timezone.utc)

JS_TIME_STRING_UTC = datetime.datetime.strftime(END_TIME_UTC, JS_TIME_STRING_UTC_FORMAT)


@bp.route('/end')
def end():
    """Handling for this in ending()"""

    return render_template(
        'timer.html',
        TIME_STRING_UTC=JS_TIME_STRING_UTC,
    )


@bp.before_app_request
def ending():
    valid = False
    # If user reached the end
    user = session.get('user')
    # If the event ended
    now = datetime.datetime.now(tz=datetime.timezone.utc)

    if (user and session['user']['end']) or (now >= END_TIME_UTC):
        if (request.endpoint not in EXEMPT_ENDPOINTS) and ('static' not in request.endpoint):
            print(request.endpoint)
            print("Trying to redirect to end")
            return redirect(url_for(END_ENDPOINT))
        return

    # If trying to access url_for('end') illegally
    if request.endpoint == END_ENDPOINT:
        print("Illegal access")
        return redirect(url_for('index'))
