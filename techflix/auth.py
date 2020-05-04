import datetime
import functools
import hashlib

# TODO: Implement method to enter debugger from any page
# TODO: Clear loophole where you can load questions and then open options to go further
from flask import (
    Blueprint, render_template, redirect, url_for, request, session, g,
)

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['POST', 'GET'])
def register():
    from .database import users

    if request.method == 'POST':
        # TODO: Check for empty userstring/password string
        username = request.form['username']

        # Validating form input
        # Checking for empty/no username
        if not username:
            return render_template('register.html', alert="Username Required")

        # # Why don't I store the password in a variable? Ineptitude derived security paranoia
        # Checking for empty/no password
        if not request.form['password']:
            return render_template('register.html', alert="Password Required")

        # Checking for username being taken
        existing_user = users.find_one({'username': username})
        if existing_user:
            return render_template('register.html', alert="That username already exists!")

        # Checking for conflicting password entries
        if request.form['password'] != request.form['confirm-password']:
            return render_template('register.html', alert="Passwords don't match!")

        hashed_password = hash_password(request.form['password'])

        users.insert_one({
            'email': request.form['email'],
            'username': username,
            'password': hashed_password,
            'score': 0,
            'time': datetime.datetime.utcnow(),
            'story_id': '1',
        })

        # Logging user in, may POST to login() later
        session['username'] = request.form['username']
        return redirect(url_for('index'))

    return render_template('register.html', alert='')


@bp.route('/login', methods=['POST', 'GET'])
def login():
    from .database import users

    username = request.form['username']

    if request.method == 'POST':
        user = users.find_one({'username': request.form['username']})
        if not user:
            return render_template('login.html', alert='Invalid Username')

        # # I might have refactored to an antipattern here
        hashed_password = hash_password(request.form['password'])
        if user['password'] != hashed_password:
            return render_template('login.html', alert='Invalid Password')

        session['username'] = request.form['username']
        return redirect(url_for('index'))

    return render_template('login.html', alert='')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# login_required decorator.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        username = session.get('username')
        if username is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view


# Password hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
