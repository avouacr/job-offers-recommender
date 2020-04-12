from flask import render_template, flash, redirect
from app_source import app
from app_source.forms import LoginForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            login_form.username.data, login_form.remember_me.data))
    return render_template('login.html', title='Identification', form=login_form)

# TODO: change login error messages to French
