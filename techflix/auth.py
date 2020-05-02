import functools
import hashlib

from flask import (
    Blueprint, render_template, redirect, url_for, request, session, g,
)

bp = Blueprint('auth', __name__)


@bp.route('/login', methods = ['POST', 'GET'])
def login():
    from .database import users

    if request.method == 'POST':
        existing_user = users.find_one({'username': request.form['username']})
        if existing_user is not None:
            hash_ = hashlib.sha256(request.form['password'].encode()).hexdigest()
            if existing_user['password'] == hash_:
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            else:
                return render_template('signin.html', alert='Invalid Username/Password')

        return render_template('signin.html', alert='Invalid Username/Password')

    return render_template('signin.html', alert='')


@bp.route('/register', methods = ['POST', 'GET'])
def register():
    from .database import users

    if request.method == 'POST':
        existing_user = users.find_one({'username': request.form['username']})
        if existing_user is None:
            if request.form['password'] == request.form['confirm-password']:
                uname = request.form['username']
                hashpass = hashlib.sha256(request.form['password'].encode()).hexdigest()
                users.insert_one({'username': uname, 'password': hashpass, 'score': 0})
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            else:
                return render_template('signup.html', alert='Passwords don\'t match!')

        return render_template('signup.html', alert='That username already exists!')

    return render_template('signup.html', alert='')


# Temporary login I needed
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
