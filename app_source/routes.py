from flask import render_template
from app_source import app
from app_source.forms import LoginForm


@app.route('/')
@app.route('/login')
def login():
    login_form = LoginForm()
    return render_template('login.html', title='Identification', form=login_form)
