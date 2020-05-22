# Blueprint which is only initialised in production

import datetime

from flask import (
    Blueprint, redirect, url_for, request, render_template
)

bp = Blueprint('deployed', __name__)


@bp.route('/countdown')
def countdown():
    return render_template('countdown.html')


@bp.before_app_request
def start():
    countdown_endpoint = "deployed.countdown"

    time_string_format = "%Y-%m-%d %H:%M:%S %z"
    target_time_string = "2020-05-25 00:00:00 +0530"

    target = datetime.datetime.strptime(target_time_string, time_string_format)

    IST_offset = datetime.timedelta(hours=5, minutes=30)
    now = datetime.datetime.now(tz=datetime.timezone(offset=IST_offset))

    if now < target:
        if request.endpoint != countdown_endpoint and 'static' not in request.endpoint:
            return redirect(url_for(countdown_endpoint))
        return
    if request.endpoint == countdown_endpoint:
        return redirect(url_for('story.story'))
