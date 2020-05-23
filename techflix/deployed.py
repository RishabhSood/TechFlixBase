# Blueprint which is only initialised in production

import datetime

from flask import (
    Blueprint, redirect, url_for, request, render_template
)

bp = Blueprint('deployed', __name__)

TIME_STRING_FORMAT = "%Y-%m-%d %H:%M:%S%z"
TARGET_TIME_STRING = "2020-05-29 00:00:00+0530"

TARGET_TIME = datetime.datetime.strptime(TARGET_TIME_STRING, TIME_STRING_FORMAT)
# IST_OFFSET = datetime.timedelta(hours=5, minutes=30)
# TIMEZONE = datetime.timezone(offset=IST_OFFSET)

TARGET_TIME_UTC = TARGET_TIME.astimezone(tz=datetime.timezone.utc)

JS_TIME_STRING_UTC_FORMAT = "%Y-%m-%dT%H:%M:%S+00:00"
JS_TIME_STRING_UTC = datetime.datetime.strftime(TARGET_TIME_UTC, JS_TIME_STRING_UTC_FORMAT)


@bp.route('/countdown')
def countdown():
    return render_template(
        'countdown.html',
        TIME_STRING_UTC=JS_TIME_STRING_UTC,
    )


@bp.before_app_request
def start():
    countdown_endpoint = "deployed.countdown"

    now = datetime.datetime.now(tz=datetime.timezone.utc)

    if now < TARGET_TIME_UTC:
        # There can be endpoint less requests, go figure
        if (request.endpoint is not None) and (request.endpoint != countdown_endpoint and 'static' not in request.endpoint):
            return redirect(url_for(countdown_endpoint))
        return
    if request.endpoint == countdown_endpoint:
        return redirect(url_for('story.story'))
