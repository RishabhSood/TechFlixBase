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

        # Ineptitude derived security paranoia makes me wonder if using password is wrong
        password = request.form['password']
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

        users.insert_one({
            'email': request.form['email'],
            'username': username,
            'password': hashed_password,
            'score': 0,
            'time': datetime.datetime.utcnow(),
            'story_id': '1',
        })

        # Logging user in
        return redirect(url_for('auth.login', username=username, password=password))

    return render_template('register.html', alert='')


@bp.route('/login', methods=['POST', 'GET'])
def login():
    from .database import users

    if request.method == 'POST':
        user = users.find_one({'username': request.form['username']})
        if not user:
            return render_template('login.html', alert='Invalid Username')

        # # I might have refactored to an antipattern here
        hashed_password = hash_password(request.form['password'])
        if user['password'] != hashed_password:
            return render_template('login.html', alert='Invalid Password')

# Object of type ObjectID is not json serializable (since it's mongo json) so it was causing issues when being stored ??
# Probably cause session is a json? Makes sense, that's why session = user passed but the return couldn't happen
# Session probably updates with the return
# Probably why the error was not in my files, because everything here actually went well
        session['user'] = {key: value for key, value in user.items() if key not in ('_id',)}
        print(session.__repr__)

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
        username = session.get('user')['username']
        if username is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view


# Password hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
