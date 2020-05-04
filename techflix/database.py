# Database connection
# Seperated as I use an app_factory but need to use import this into the others
# Might try importing into app_factory and then ading into session or something.

from flask import (
    current_app,
)

from flask_pymongo import PyMongo

mongo = PyMongo(current_app)

users = mongo.db.users
question_bank = mongo.db.questions
storyline = mongo.db.story
optionline = mongo.db.options
