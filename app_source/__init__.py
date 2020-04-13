from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config) # Get configuration from the Config class
db = SQLAlchemy(app) # Instantiate database
login = LoginManager(app) # Instantiate login manager (for session suspension)
login.login_view = 'login' # Make access to the app only possible to logged in users

# Import routes at the bottom to avoid circular imports
from app_source import routes, models