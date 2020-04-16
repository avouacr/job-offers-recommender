from flask import render_template, flash, redirect, url_for, request
from app_source import app, models
from app_source.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app_source.models import User
from werkzeug.urls import url_parse


@app.route('/')
def root():
    if current_user.is_authenticated:
        # Prevent already logged in users to access login page again
        return redirect(url_for('main'))
    else:
        return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        # Don't allow already logged in users to access login page again
        return redirect(url_for('main'))
    login_form = LoginForm()

    if login_form.validate_on_submit():
        # Check if user exists in the db, and if the password is correct
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Utilisateur inconnu ou mot de passe invalide.')
            return redirect(url_for('login'))
        # Register the user as logged in and display main page of the app
        login_user(user)
        # Redirect to the page requested before login, if any
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main')
        return redirect(next_page)

    return render_template('login.html', title='Identification', form=login_form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        models.db.session.add(user)
        models.db.session.commit()
        flash('Inscription terminée. Vous pouvez désormais vous identifier.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/main/')
@login_required
def main():
    return render_template('main.html', title="Page d'accueil")


@app.route('/profil_info_generales/', methods=['GET', 'POST'])
@login_required
def profil_info_generales():
    form = GeneralInfoForm()
    if form.is_submitted():
        if form.add_language.data:
            form.languages.append_entry()
        elif form.remove_language.data:
            form.languages.pop_entry()
        elif form.submit.data:
            if form.validate():
                return redirect(url_for('profil_certifications'))
    return render_template('profil_info_generales.html',
                           title="Profil - Informations générales",
                           form=form)


@app.route('/profil_certifications/', methods=['GET', 'POST'])
@login_required
def profil_certifications():
    form = CertificationsForm()
    if form.is_submitted():
        if form.add_license.data:
            form.driver_licenses.append_entry()
        elif form.remove_license.data:
            form.driver_licenses.pop_entry()
        elif form.add_other_certif.data:
            form.other_certifications.append_entry()
        elif form.remove_other_certif.data:
            form.other_certifications.pop_entry()
        elif form.submit.data:
            if form.validate():
                return redirect(url_for('profil_formation'))
    return render_template('profil_certifications.html',
                           title="Profil - Certifications",
                           form=form)


@app.route('/profil_formation/', methods=['GET', 'POST'])
@login_required
def profil_formation():
    form = FormationForm()
    if form.is_submitted():
        if form.add_formation.data:
            form.formation_entries.append_entry()
        elif form.remove_formation.data:
            form.formation_entries.pop_entry()
        elif form.submit.data:
            if form.validate():
                return redirect(url_for('profil_experience'))
    return render_template('profil_formation.html',
                           title="Profil - Formation",
                           form=form)


@app.route('/profil_experience/', methods=['GET', 'POST'])
@login_required
def profil_experience():
    form = ExperienceForm()
    if form.is_submitted():
        if form.add_experience.data:
            form.experience_entries.append_entry()
        elif form.remove_experience.data:
            form.experience_entries.pop_entry()
        elif form.submit.data:
            if form.validate():
                return redirect(url_for('main'))
    return render_template('profil_experience.html',
                           title="Profil - Expérience",
                           form=form)


@app.route('/generation_cv/')
@login_required
def generation_cv():
    return render_template('generation_cv.html', title="Génération de CV")


@app.route('/offres_recommandees/')
@login_required
def offres_recommandees():
    return render_template('offres_recommandees.html', title="Offres recommandées")
