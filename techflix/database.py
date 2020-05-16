# Database connection
# Seperated as I use an app_factory but need to use import this into the others
# Might try importing into app_factory and then ading into session or something.

from flask import (
    current_app,
)
import flask_pymongo

mongo = flask_pymongo.PyMongo(current_app)

# TODO: Ask for help with database stuff
# Apparently only one connection is created at a time..
# with open('log.txt', 'a') as log_file:
#     print('1 Connection created', file=log_file)  # dev

users = mongo.db.users
question_bank = mongo.db.questions
storyline = mongo.db.story
optionline = mongo.db.options

# Debug this later, moved to story.py for now
# leaderboard = users.find().sort([("score", flask_pymongo.DESCENDING), ("time", flask_pymongo.ASCENDING)])
