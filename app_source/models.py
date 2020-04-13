from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app_source import app, login

# Instantiate database
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    """Table to store user data from registration."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<Utilisateur {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    """Helper function to access the data of a given user."""
    return User.query.get(int(id))


class JobOffers(db.Model):
    """Table to store job offers data."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(120))
    # TODO: add all relevant fields
    # TODO: set appropriate string lengths by looking at actual max lengths


def init_db():
    """Perform database (re)initialization."""
    db.drop_all()
    db.create_all()
    db.session.commit()
    print('Database initialized.')
