from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dynaconf import FlaskDynaconf

app = Flask(__name__)
FlaskDynaconf(app, settings_files=["settings.toml", ".secrets.toml"])

db = SQLAlchemy()
db.init_app(app)

# Importa as rotas depois de criar o app e o banco.
import routes  # noqa: E402,F401

with app.app_context():
    db.create_all()
