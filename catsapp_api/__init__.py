from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app) # Ingest Data via models
migrate = Migrate(app,db) # Ingest Data via models
ma = Marshmallow(app) # Digest Data via models

login_manager = LoginManager(app)

from catsapp_api import models, routes