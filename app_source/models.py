from app_source import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<Utilisateur {}>".format(self.email)


class JobOffers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    description = db.Column(db.String(120))
    # TODO: set appropriate string lengths by looking at the actual max length
    # TODO: add all relevant fields