import logging
import os
import tempfile
from datetime import date
import json

import numpy as np
import pandas as pd

from flask import render_template, flash, redirect, url_for, request, send_file
from flask_login import current_user, login_user, logout_user, login_required
from sklearn.metrics.pairwise import cosine_similarity
# from app_source.models import JobOffers, OfferVectors
from werkzeug.urls import url_parse

from app_source import app, models
from app_source.forms import CertificationsForm, FormationForm, ExperienceForm
from app_source.forms import LoginForm, RegistrationForm, GeneralInfoForm
from app_source.forms import SkillsForm, PresentationForm
from app_source.models import Formation, Experience, ComputerSkills, OtherSkills
from app_source.models import Presentation, ProfilCompleted
from app_source.models import User, SpokenLanguages, DriverLicenses, OtherCertifications
# from app_source.models import JobOffers, OfferVectors
from werkzeug.urls import url_parse
from sklearn.metrics.pairwise import cosine_similarity

from cv_generator import cv_generator
from cv_generator.cv_generator.themes.developer import ThemeDeveloper


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
        # If form is validated, populate user table with registration info
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
        # Buttons to add/remove a language subform
        if form.add_language.data:
            form.languages.append_entry()
        elif form.remove_language.data and form.languages.data:
            form.languages.pop_entry()
        elif form.validate():

            # Add general info to user table
            user_id = current_user.id
            user = User.query.filter_by(id=user_id).first()
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.phone_number = form.phone_number.data
            user.postal_code = form.postal_code.data
            user.city = form.city.data
            user.mobility = form.mobility.data

            # Populate SpokenLanguages table
            for subform in form.languages.data:
                language = subform['language']
                level = subform['level']
                entry = SpokenLanguages(language=language,
                                        level=level,
                                        user_id=user_id)
                models.db.session.add(entry)

            models.db.session.commit()
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
        elif form.remove_license.data and form.driver_licenses.data:
            form.driver_licenses.pop_entry()

        elif form.add_other_certif.data:
            form.other_certifications.append_entry()
        elif form.remove_other_certif.data and form.other_certifications.data:
            form.other_certifications.pop_entry()

        elif form.submit.data:
            if form.validate():
                user_id = current_user.id

                # Populate DriverLicenses table
                for subform in form.driver_licenses.data:
                    license_type = subform['driver_license']
                    entry = DriverLicenses(license_type=license_type,
                                           user_id=user_id)
                    models.db.session.add(entry)

                # Populate OtherCertifications table
                for subform in form.other_certifications.data:
                    other_certif = subform['other_certif']
                    entry = OtherCertifications(other_certif=other_certif,
                                                user_id=user_id)
                    models.db.session.add(entry)

                models.db.session.commit()
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
        elif form.remove_formation.data and form.formation_entries.data:
            form.formation_entries.pop_entry()
        elif form.submit.data:
            if form.validate():
                user_id = current_user.id

                # Populate Education table
                for subform in form.formation_entries.data:
                    start_date = subform['date_start']
                    end_date = subform['date_end']
                    institution = subform['institution']
                    title = subform['title']
                    description = subform['desc']
                    entry = Formation(start_date=start_date,
                                      end_date=end_date,
                                      institution=institution,
                                      title=title,
                                      description=description,
                                      user_id=user_id)
                    models.db.session.add(entry)

                models.db.session.commit()
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
        elif form.remove_experience.data and form.experience_entries.data:
            form.experience_entries.pop_entry()
        elif form.submit.data:
            if form.validate():
                user_id = current_user.id

                # Populate Experience table
                for subform in form.experience_entries.data:
                    start_date = subform['date_start']
                    end_date = subform['date_end']
                    institution = subform['institution']
                    title = subform['title']
                    description = subform['desc']
                    is_relevant = subform['is_relevant']
                    entry = Experience(start_date=start_date,
                                       end_date=end_date,
                                       institution=institution,
                                       title=title,
                                       description=description,
                                       relevant_for_jobsearch=is_relevant,
                                       user_id=user_id)
                    models.db.session.add(entry)

                # Keep track when users has completed their profile
                entry = ProfilCompleted(completed=True, user_id=user_id)
                models.db.session.add(entry)

                models.db.session.commit()
                return redirect(url_for('profil_competences'))
    return render_template('profil_experience.html',
                           title="Profil - Expérience",
                           form=form)


@app.route('/profil_competences/', methods=['GET', 'POST'])
@login_required
def profil_competences():
    form = SkillsForm()
    if form.is_submitted():
        # Buttons to add/remove a skill
        if form.add_computer_skill.data:
            form.computer_skills.append_entry()
        elif form.remove_computer_skill.data and form.computer_skills.data:
            form.computer_skills.pop_entry()
        if form.add_other_skill.data:
            form.other_skills.append_entry()
        elif form.remove_other_skill.data and form.other_skills.data:
            form.other_skills.pop_entry()
        elif form.submit.data:
            if form.validate():
                user_id = current_user.id

                # Populate ComputerSkills table
                for subform in form.computer_skills.data:
                    computer_skill = subform['computer_skill']
                    entry = ComputerSkills(skill=computer_skill,
                                           user_id=user_id)
                    models.db.session.add(entry)

                # Populate OtherSkills table
                for subform in form.other_skills.data:
                    other_skill = subform['other_skill']
                    entry = OtherSkills(skill=other_skill,
                                        user_id=user_id)
                    models.db.session.add(entry)

                models.db.session.commit()
                return redirect(url_for('profil_presentation'))

    return render_template('profil_competences.html',
                           title="Profil - Informations générales",
                           form=form)


@app.route('/profil_presentation/', methods=['GET', 'POST'])
@login_required
def profil_presentation():
    form = PresentationForm()
    if form.validate_on_submit():
        entry = Presentation(presentation=form.presentation.data,
                             user_id=current_user.id)
        models.db.session.add(entry)
        models.db.session.commit()
        return redirect(url_for('main'))

    return render_template('profil_presentation.html',
                           title="Profil - Présentation!",
                           form=form)


@app.route('/generation_cv/')
@login_required
def generation_cv():
    # Print error message if the user has not completed his profile yet
    user_id = current_user.id
    has_completed = ProfilCompleted.query.filter_by(user_id=user_id).first()
    if has_completed is None:
        flash("Vous devez d'abord compléter votre profil.")
        return redirect(url_for('main'))

    # Initialize dictionary that holds CV info
    cv_dict = {
        'lang': "fr-FR",
        'last_update': date.today().strftime("%Y-%m-%d"),
    }

    # Add general user info
    user = User.query.filter_by(id=user_id).first()
    cv_dict['basic'] = {
        'name': user.first_name,
        'surnames': user.last_name,
        'residence': user.city,
        'disponibilite_geographique': user.mobility,
    }
    presentation = Presentation.query.filter_by(id=user_id).first()
    if presentation is not None:
        cv_dict['basic']['biography'] = presentation.presentation
    cv_dict['contact'] = {
        'email': user.username,
        'phone': user.phone_number
    }

    # Add spoken languages
    languages_query = SpokenLanguages.query.filter_by(user_id=user_id).all()
    languages_entries = []
    for entry in languages_query:
        dic_entry = {'name': entry.language + ' : ' + entry.level}
        languages_entries.append(dic_entry)
    if languages_entries:
        cv_dict['languages'] = languages_entries
    else:
        cv_dict['languages'] = []

        # Add certifications
    licenses_query = DriverLicenses.query.filter_by(user_id=user_id).all()
    other_certif_query = OtherCertifications.query.filter_by(user_id=user_id).all()
    certifications_entries = []
    for entry in licenses_query:
        dic_entry = {'name': 'Permis ' + entry.license_type}
        certifications_entries.append(dic_entry)
    for entry in other_certif_query:
        dic_entry = {'name': entry.other_certif}
        certifications_entries.append(dic_entry)
    if certifications_entries:
        cv_dict['certifications'] = certifications_entries
    else:
        cv_dict['certifications'] = []

        # Add education
    education_query = Formation.query.filter_by(user_id=user_id).all()
    education_entries = []
    for entry in education_query:
        dic_entry = {
            'institution': entry.institution,
            'degree': entry.title,
            'date_start': entry.start_date,
            'date_end': entry.end_date,
            'description': entry.description
        }
        education_entries.append(dic_entry)
    if education_entries:
        cv_dict['education'] = education_entries
    else:
        cv_dict['education'] = []

        # Add experience
    experience_query = Experience.query.filter_by(user_id=user_id).all()
    experience_entries = []
    for entry in experience_query:
        dic_entry = {
            'institution': entry.institution,
            'position': entry.title,
            'date_start': entry.start_date,
            'date_end': entry.end_date,
            'description': entry.description
        }
        experience_entries.append(dic_entry)
    if experience_entries:
        cv_dict['experience'] = experience_entries
    else:
        cv_dict['experience'] = []

    # Add skills section
    it_skills_query = ComputerSkills.query.filter_by(user_id=user_id).all()
    other_skills_query = OtherSkills.query.filter_by(user_id=user_id).all()
    skills_entries = []
    for entry in it_skills_query:
        dic_entry = {'name': entry.skill}
        skills_entries.append(dic_entry)
    for entry in other_skills_query:
        dic_entry = {'name': entry.skill}
        skills_entries.append(dic_entry)
    if skills_entries:
        cv_dict['informatique'] = skills_entries
    else:
        cv_dict['informatique'] = []

        # Create a logging.Logger object to be used in the CV generation
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger('cv_generator')
    logger.propagate = True

    # Generate CV
    cv_schema_path = 'cv_generator/cv.schema.json'
    cv = cv_generator.CV(logger).load(cv_dict, cv_schema_path)
    themes_dict = {
        'developer': ThemeDeveloper,
    }
    theme = themes_dict['developer'](cv, logger)

    # Store generated CV in a temp directory
    file_name = user.last_name.lower() + '_' + user.first_name.lower()
    file_name_full = file_name + '.pdf'
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = tmpdir + os.sep + '{}'.format(file_name)
        file_path_full = file_path + '.pdf'
        theme.save(file_path, keep_tex=False)
        return send_file(file_path_full,
                         mimetype='application/pdf',
                         attachment_filename=file_name_full,
                         as_attachment=True)


@app.route('/offres_recommandees/')
@login_required
def offres_recommandees():
    # Print error message if the user has not completed his profile yet
    user_id = current_user.id
    has_completed = ProfilCompleted.query.filter_by(user_id=user_id).first()
    if has_completed is None:
        flash("Vous devez d'abord compléter votre profil.")
        return redirect(url_for('main'))

    # Compute representations of user description and relevant experiences
    presentation = Presentation.query.filter_by(id=user_id).first().presentation
    exp_entries = Experience.query.filter_by(user_id=user_id).all()
    experiences_description = [x.description for x in exp_entries
                               if x.relevant_for_jobsearch]
    relevant_texts = [presentation] + experiences_description
    from doc_embeddings import fasttext_embeddings
    relevant_vectors = fasttext_embeddings.compute_vectors(relevant_texts, n_jobs=1)

    # Compute similarities with job offers representations
    df_offers = pd.read_csv('data/all_offers_nodup_test.csv')
    offer_vectors = np.load('data/offers_fasttext.npy')

    # Filter offers according to the user's mobility radius
    user = User.query.filter_by(id=user_id).first()
    cp_user = user.postal_code
    mobility_user = user.mobility

    if mobility_user == 'Ville':
        idx = df_offers.index[df_offers['localisation'] == cp_user].tolist()
    elif mobility_user == 'Département':
        idx = df_offers.index[df_offers['localisation'].str[:2] == cp_user[:2]].tolist()
    elif mobility_user == 'Région':
        with open('data/dict_dpt_region.json', 'r') as fp:
            dict_dpt_region = json.load(fp)
        region_user = dict_dpt_region[cp_user[:2]]
        dpt_list = [d for d in dict_dpt_region.keys()
                    if dict_dpt_region[d] == region_user]
        idx = df_offers.index[((df_offers['localisation'].str[:2].isin(dpt_list))
                               | (df_offers['localisation'] == region_user))].tolist()
    elif mobility_user == 'France entière':
        idx = df_offers.index.tolist()

    df_offers = df_offers[df_offers.index.isin(idx)]
    offer_vectors = offer_vectors[idx]
    assert df_offers.shape[0] == offer_vectors.shape[0]

    # Compute all pairwise similarities
    similarities = cosine_similarity(relevant_vectors, offer_vectors)

    # Rank job offers by similarity with the user info
    similarities_indices = list(zip(similarities.ravel(),
                                    list(range(similarities.shape[1])) * similarities.shape[0]))
    similarities_ranked = sorted(similarities_indices, key=lambda x: x[0], reverse=True)
    indices_ranked = [x[1] for x in similarities_ranked]

    # Keep unique ranks (i.e. sort offers by decreasing cosine similarity with user info)
    unique_ranks = []
    for n in indices_ranked:
        if n not in unique_ranks:
            unique_ranks.append(n)


    final_df = df_offers.reindex(unique_ranks)[:40]

    # return render_template('recommended_offers.html', title="Offres recommandées",
    #                        results=final_df.id)
    return render_template('recommended_offers.html', title="Offres recommandées",
                           df=final_df)

