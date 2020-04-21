from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms import TextAreaField, SelectField, FieldList, FormField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.validators import Length
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


class SpokenLanguagesSubform(FlaskForm):

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
    first_name = StringField('Prénom', validators=[DataRequired()])
    last_name = StringField('Nom', validators=[DataRequired()])
    phone_number = StringField('Numéro de téléphone', validators=[DataRequired()])
    postal_code = StringField('Code postal', validators=[DataRequired(),
                                                         Length(min=5, max=5)])
    city = StringField('Ville de résidence', validators=[DataRequired()])
    mobility_choices = ['Ville', 'Département', 'Région', 'France entière']
    mobility = SelectField('Mobilité',
    	choices=list(zip(mobility_choices, mobility_choices)))
    languages = FieldList(FormField(SpokenLanguagesSubform),
                          min_entries=1, max_entries=5)
    add_language = SubmitField('Ajouter une langue')
    remove_language = SubmitField('Retirer une langue')
    submit = SubmitField('Valider et continuer')


class DriverLicensesSubform(FlaskForm):

    class Meta:
        csrf = False

    with open('data/french_driver_licenses.txt', 'r') as f:
        licenses = f.read().splitlines()[:-1]
    licenses = sorted(licenses)
    license_choices = list(zip(licenses, licenses))
    driver_license = SelectField('Permis', choices=license_choices)


class OtherCertificationsSubform(FlaskForm):

    class Meta:
        csrf = False

    other_certif = StringField('Autre certification')


class CertificationsForm(FlaskForm):

    driver_licenses = FieldList(FormField(DriverLicensesSubform),
                                min_entries=0, max_entries=10)
    add_license = SubmitField('Ajouter un permis')
    remove_license = SubmitField('Retirer un permis')
    other_certifications = FieldList(FormField(OtherCertificationsSubform),
                                     min_entries=0, max_entries=10)
    add_other_certif = SubmitField('Ajouter une certification')
    remove_other_certif = SubmitField('Retirer une certification')
    submit = SubmitField('Valider et continuer')


class FormationExpererienceSubform(FlaskForm):

    class Meta:
        csrf = False

    date_start = DateField('Date de début', format='%m/%Y',
                           validators=[DataRequired()])
    date_end = DateField('Date de fin', format='%m/%Y',
                         validators=[DataRequired()])
    title = StringField('Titre', validators=[DataRequired()])
    institution = StringField('Établissement', validators=[DataRequired()])
    desc = TextAreaField('Description', render_kw={"rows": 5, "cols": 50})
    is_relevant = BooleanField("Cette expérience est pertinente pour ma recherche d'emploi actuelle")


class FormationForm(FlaskForm):

    formation_entries = FieldList(FormField(FormationExpererienceSubform),
                                  min_entries=0, max_entries=10)
    add_formation = SubmitField('Ajouter une formation')
    remove_formation = SubmitField('Retirer une formation')
    submit = SubmitField('Valider et continuer')


class ExperienceForm(FlaskForm):

    experience_entries = FieldList(FormField(FormationExpererienceSubform),
                                   min_entries=0, max_entries=10)
    add_experience = SubmitField('Ajouter une expérience')
    remove_experience = SubmitField('Retirer une expérience')
    submit = SubmitField('Valider et continuer')


class ComputerSkillsSubform(FlaskForm):

    class Meta:
        csrf = False

    computer_skill = StringField('Outil informatique')


class OtherSkillsSubform(FlaskForm):

    class Meta:
        csrf = False

    other_skill = StringField('Outil informatique')


class SkillsForm(FlaskForm):
    """Form object to store skills of the user."""
    computer_skills = FieldList(FormField(ComputerSkillsSubform),
                                min_entries=0, max_entries=10)
    add_computer_skill = SubmitField('Ajouter une compétence')
    remove_computer_skill = SubmitField('Retirer une compétence')
    other_skills = FieldList(FormField(OtherSkillsSubform),
                             min_entries=0, max_entries=10)
    add_other_skill = SubmitField('Ajouter une compétence')
    remove_other_skill = SubmitField('Retirer une compétence')
    submit = SubmitField('Valider et continuer')


class PresentationForm(FlaskForm):
    """Form object to store the user self presentation."""
    presentation = TextAreaField('Présentation', render_kw={"rows": 5, "cols": 50},
                                 validators=[DataRequired()])
    submit = SubmitField('Valider et terminer')
