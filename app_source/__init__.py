from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config) # Get configuration from the Config class
db = SQLAlchemy(app) # Instantiate database
# Instantiate migration engine (makes future data migration much easier)
migrate = Migrate(app, db)

# Import routes at the bottom to avoid circular imports
from app_source import routes, models