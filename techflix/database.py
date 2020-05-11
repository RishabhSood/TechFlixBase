# Database connection
# Seperated as I use an app_factory but need to use import this into the others
# Might try importing into app_factory and then ading into session or something.

from flask import (
    current_app,
)
import flask_pymongo

mongo = flask_pymongo.PyMongo(current_app)
with open('log.txt', 'a') as log_file:
    print('1 Connection created', file=log_file)  # d
with open('log.txt', 'a') as log_file:
    print('2 Connection created', file=log_file)  # d

users = mongo.db.users
question_bank = mongo.db.questions
storyline = mongo.db.story
optionline = mongo.db.options

leaderboard = users.find().sort([("score", flask_pymongo.DESCENDING), ("time", flask_pymongo.ASCENDING)])
