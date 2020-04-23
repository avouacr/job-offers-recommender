from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# import pandas as pd
# from multiprocessing import cpu_count

from app_source import app, login

# Instantiate database
db = SQLAlchemy(app)

def init_db():
    """Helper function to perform database (re)initialization."""
    db.drop_all()
    db.create_all()
    db.session.commit()


class User(UserMixin, db.Model):
    """Table to store user data from registration."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone_number = db.Column(db.String(64))
    postal_code = db.Column(db.String(10))
    city = db.Column(db.String(64))
    mobility = db.Column(db.String(64))

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
    relevant_for_jobsearch = db.Column(db.Boolean())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class ComputerSkills(db.Model):
    """Table to store the IT skills of the user."""
    id = db.Column(db.Integer, primary_key=True)
    skill = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class OtherSkills(db.Model):
    """Table to store other skills of the user."""
    id = db.Column(db.Integer, primary_key=True)
    skill = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Presentation(db.Model):
    """Table to store user self-description."""
    id = db.Column(db.Integer, primary_key=True)
    presentation = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class ProfilCompleted(db.Model):
    """Table to test whether users have completed their profile."""
    id = db.Column(db.Integer, primary_key=True)
    completed = db.Column(db.Boolean())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# class JobOffers(db.Model):
#     """Table to store job offers data."""
#     id = db.Column(db.String(10), primary_key=True)
#     intitule = db.Column(db.Text())
#     description = db.Column(db.Text())
#
#
# class OfferVectors(db.Model):
#     """Table to store job offers vector representations."""
#     id = db.Column(db.Integer, primary_key=True)
#     vector = db.Column(db.Text())
#     offer_id = db.Column(db.String(10), db.ForeignKey('job_offers.id'))
#
#
# def update_job_offers():
#     """Helper function to periodically update job offers data."""
#
#     # Import current job offers
#     df_offers = pd.read_csv('data/all_offers.csv')
#
#     # Remove outdated offers from db
#     ids_in_db = [x[0] for x in JobOffers.query.with_entities(JobOffers.id).all()]
#     ids_to_remove = [id for id in ids_in_db if id not in df_offers.id.values]
#     for id in ids_to_remove:
#         JobOffers.query.filter_by(id=id).delete()
#         OfferVectors.query.filter_by(offer_id=id).delete()
#     db.session.commit()
#     ids_in_db = [x[0] for x in JobOffers.query.with_entities(JobOffers.id).all()]
#
#     # Process new job offers
#     ids_to_add = [id for id in df_offers.id.values if id not in ids_in_db]
#
#     # Compute document vectors
#     print('Importing FastText model.')
#     from doc_embeddings import fasttext_embeddings
#     df_new_offers = df_offers[df_offers.id.isin(ids_to_add)]
#     print('Computing FastText representations of job offers.')
#     new_vectors = fasttext_embeddings.compute_vectors(df_new_offers['description'].values,
#                                                       n_jobs=cpu_count())
#
#     # Add new offers to db
#     print('Adding new offers to database.')
#     entries = []
#     for i, vec in enumerate(new_vectors):
#         row = df_new_offers.iloc[i]
#         entries.append(JobOffers(id=row.id, intitule=row.intitule,
#                                        description=row.description))
#         entries.append(OfferVectors(vector=str(list(vec)),
#                                     offer_id=row.id))
#         if (i % 1000 == 0) & (i > 0):
#             # Add entries by bulk to prevent session overload
#             db.session.add_all(entries)
#             db.session.commit()
#             entries = []
#
#     db.session.add_all(entries)
#     db.session.commit()


def populate_db_test():

    entries = []

    entries.append(User(
        id=1,
        username='romain.avouac@ensae.fr',
        password_hash='pbkdf2:sha256:150000$C63gRD2m$c498dba396ce36403c8be70951a4e2a1a15026e61644ffa4aefbdc874938e6d7',
        first_name='Romain',
        last_name='Avouac',
        phone_number='0669120021',
        postal_code='75013',
        city='Paris',
        mobility='Département'
    ))

    entries.append(SpokenLanguages(
        language='Français',
        level='Langue maternelle',
        user_id=1
    ))

    entries.append(SpokenLanguages(
        language='Anglais',
        level='Avancé',
        user_id=1
    ))

    entries.append(DriverLicenses(
        license_type='B',
        user_id=1
    ))

    entries.append(DriverLicenses(
        license_type='A1',
        user_id=1
    ))

    entries.append(OtherCertifications(
        other_certif='CAP Patissier',
        user_id=1
    ))

    entries.append(Formation(
        start_date='2019-06-01',
        end_date='2020-06-01',
        institution='École Polytechnique',
        title='M2 Data Science',
        description='Master degree in data science.',
        user_id=1
    ))

    entries.append(Experience(
        start_date='2019-06-01',
        end_date='2019-09-01',
        institution='Foundamental',
        title='Stagiaire',
        description="""Création d’un outil de détection de la similarité entre entreprises à
partir d’algorithmes de traitement automatique du langage naturel
et d’apprentissage statistique supervisé et non-supervisé.""",
        relevant_for_jobsearch=1,
        user_id=1
    ))

    entries.append(Experience(
        start_date='2018-09-01',
        end_date='2019-05-01',
        institution='INSEE, SSP-Lab',
        title='Stagiaire',
        description="""Amélioration de l’estimation de la population présente à partir des
données de téléphonie mobile via un modèle bayésien de détection
géographique des évènements..""",
        relevant_for_jobsearch=1,
        user_id=1
    ))

    entries.append(ComputerSkills(
        skill='LaTeX',
        user_id=1
    ))

    entries.append(ComputerSkills(
        skill='QGIS',
        user_id=1
    ))

    entries.append(OtherSkills(
        skill='PIMP',
        user_id=1
    ))

    pres = """Étudiant en statistiques à l’ENSAE Paris-Tech et en économie 
        à l’ENS Paris-Saclay, je suis passionné par la science des données, notamment par
        les enjeux liés à l’exploitation des données massives. Je participe également à
         la recherche en sciences sociales, notamment dans le cadre d’un projet visant
    à caractériser l’évolution de la composition sociale des populations étudiantes au sein
    des établissements d’enseignement supérieur français."""
    pres = pres.replace('\n', ' ')

    entries.append(Presentation(
        presentation=pres,
        user_id=1
    ))

    entries.append(ProfilCompleted(
        completed=1,
        user_id=1
    ))

    db.session.add_all(entries)
    db.session.commit()
