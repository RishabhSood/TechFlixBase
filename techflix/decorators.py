import functools

from flask import (
    session, redirect, url_for
)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        user = session.get('user')
        if user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view


def logout_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        user = session.get('user')
        if user:
            return redirect(url_for('story.story'))
        return view(**kwargs)

    return wrapped_view
