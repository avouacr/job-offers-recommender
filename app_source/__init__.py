from flask import Flask
from config import Config
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config) # Get configuration from the Config class

login = LoginManager(app) # Instantiate login manager (for session suspension)
login.login_view = 'login' # Make access to the app only possible to logged in users

# Import routes and models at the bottom to avoid circular imports
from app_source import routes, models, errors
models.db.init_app(app) # Connect database to the app
models.init_db() # Initialize SQL database

app.static_folder = 'static'

@app.cli.command('init_db')
def init_db():
    """Enable database (re)initialization."""
    models.init_db()

@app.cli.command('update_job_offers')
def update_job_offers():
    """Update job offers using newly scraped data."""
    models.update_job_offers()
