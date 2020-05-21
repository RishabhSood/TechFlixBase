import datetime
import functools
import hashlib

from flask import (
    Blueprint, render_template, redirect, url_for, request, session, g,
)


# Functions:
# Password hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Decorators:
# login_required decorator.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        user = session.get('user')
        if user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view


# # Probably should make this and login required one function
# logout_required decorator
def logout_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        user = session.get('user')
        if user:
            return redirect(url_for('story.story'))
        return view(**kwargs)

    return wrapped_view


# Blueprint:
bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['POST', 'GET'])
@logout_required
def register():
    from .database import users

    if request.method == 'POST':
        # Validating form input
        username = request.form['username']
        password = request.form['password']

        # Checking for empty/no username
        if not username:
            return render_template('register.html', alert="Username Required")

        # Checking for empty/no password
        if not password:
            return render_template('register.html', alert="Password Required")

        # Checking for username being taken
        existing_user = users.find_one({'username': username})
        if existing_user:
            return render_template('register.html', alert="That username already exists!")

        # Checking for conflicting password entries
        if password != request.form['confirm-password']:
            return render_template('register.html', alert="Passwords don't match!")

        hashed_password = hash_password(password)

        # Entering user into database
        users.insert_one({
            'email': request.form['email'],
            'username': username,
            'password': hashed_password,
            'score': 0,
            'time': datetime.datetime.utcnow(),
            'story_id': '1',
            'answered': False,
        })

        # Logging user in
        return redirect(url_for('auth.login', username=username, password=password))

    return render_template('register.html', alert='')


@bp.route('/login', methods=['POST', 'GET'])
@logout_required
def login():
    from .database import users

    if request.method == 'POST':
        # Validating user
        user = users.find_one({'username': request.form['username']})
        if not user:
            return render_template('login.html', alert='Invalid Username')

        # # I might have refactored to an antipattern here
        hashed_password = hash_password(request.form['password'])
        if user['password'] != hashed_password:
            return render_template('login.html', alert='Invalid Password')

        # Loading user details into session
        session['user'] = {key: value for key, value in user.items() if key not in ('_id',)}

        return redirect(url_for('index'))

    return render_template('login.html', alert='')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

