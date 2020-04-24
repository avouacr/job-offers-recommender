"""Config file for the Flask app.

NB : this file is committed only to allow general testing of the app.
In a production environment, it should never be committed.
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uJxcaiIy3Zr8tbVg%qE85A54I2PBWqWN7XQfRAT6s^'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False