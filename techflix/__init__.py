# -*- coding: utf-8 -*-
"""
Created on Fri May  1 11:14:06 2020

@author: soodr
"""
import os

from flask import (
    Flask, render_template, redirect, url_for, session
)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # TODO: Move to instance-only/env-var database_uri
    # Database Config
    app.config['MONGO_URI'] = (
        '***REMOVED***'
    )

    # Load correct config
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Blueprints:
    # Authentication
    from . import auth
    app.register_blueprint(auth.bp)

    # Story/game  # Commented out pending functional implementation of story.py
    from . import story
    app.register_blueprint(story.bp)

    # Easier debugging
    if app.config['DEBUG']:
        @app.route('/debug')
        def debug():
            # Run in debug console to get app_context.
            # from . import create_app
            # debug_app = create_app()
            # Useful for accessing, e.g, debug_app.config
            raise ValueError

    # Root route
    @app.route('/')
    def index():
        if 'username' in session:
            return redirect(url_for('story.story'))

        return render_template('home.html')

    return app
