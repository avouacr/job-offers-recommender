from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app_source import app, login

# Instantiate database
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    """Table to store user data from registration."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone_number = db.Column(db.String(64))
    city = db.Column(db.String(64))
    mobility = db.Column(db.String(64))
    description = db.Column(db.Text())

    def __repr__(self):
        return "<Utilisateur {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    """Helper function to access the data of a logged user."""
    return User.query.get(int(id))


class SpokenLanguages(db.Model):
    """Table to store the languages spoken by the user."""
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(128))
    level = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class DriverLicenses(db.Model):
    """Table to store the driver licenses owned by the user."""
    id = db.Column(db.Integer, primary_key=True)
    license_type = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class OtherCertifications(db.Model):
    """Table to store the other certifications owned by the user."""
    id = db.Column(db.Integer, primary_key=True)
    other_certif = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Formation(db.Model):
    """Table to store the education of the user."""
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    institution = db.Column(db.String(128))
    title = db.Column(db.String(128))
    description = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Experience(db.Model):
    """Table to store the professional experiences of the user."""
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    institution = db.Column(db.String(128))
    title = db.Column(db.String(128))
    description = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class JobOffers(db.Model):
    """Table to store job offers data."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(120))
    # TODO: add all relevant fields
    # TODO: set appropriate string lengths by looking at actual max lengths


def init_db():
    """Helper function to perform database (re)initialization."""
    db.drop_all()
    db.create_all()
    db.session.commit()
    print('Database initialized.')
