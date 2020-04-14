from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import TextAreaField, SelectField, FieldList, FormField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app_source.models import User


class LoginForm(FlaskForm):
    """Form object to enable user login."""
    username = StringField("Adresse électronique", validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Connexion')


class RegistrationForm(FlaskForm):
    """Form object to enable user registration."""
    username = StringField('Adresse électronique', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    password2 = PasswordField(
        'Répéter le mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Valider")

    def validate_username(self, username):
        """Check if a user is already registered in the database."""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Cette adresse électronique a déjà été utilisée.')


class SpokenLanguagesForm(FlaskForm):

    class Meta:
        csrf = False

    with open('data/languages_list.txt', 'r') as f:
        languages = f.read().splitlines()[:-1]
    languages = sorted(languages)
    language_choices = list(zip(languages, languages))
    language = SelectField('Langue', choices=language_choices)
    levels = ['Débutant', 'Intermédiaire', 'Avancé', 'Langue maternelle']
    level_choices = list(zip(levels, levels))
    level = SelectField('Niveau', choices=level_choices)

class GeneralInfoForm(FlaskForm):
    """Form object to store general informations about the user."""

    class Meta:
        csrf = False
    # TODO : understand the "The CSRF token is missing." error whithout it.

    first_name = StringField('Prénom', validators=[DataRequired()])
    last_name = StringField('Nom', validators=[DataRequired()])
    phone_number = StringField('Numéro de téléphone', validators=[DataRequired()])
    city = StringField('Ville de résidence', validators=[DataRequired()])
    license = BooleanField('Permis B')
    mobility = SelectField('Mobilité',
    	choices=[
    	('city', 'Ville'), 
    	('dpt', 'Département'), 
    	('region', 'Région'),
    	('ntn', 'France entière')
    	])
    languages = FieldList(FormField(SpokenLanguagesForm),
                          min_entries=1,
                          max_entries=10)
    add_language = SubmitField('Ajouter une langue')
    description = TextAreaField('Présentation')
    submit = SubmitField('Valider et continuer')
