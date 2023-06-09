"""visualizer set up
"""
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_login import LoginManager
# from flask_wtf.csrf import CSRFProtect
from flask.logging import create_logger

import logging

from logging.config import dictConfig

logging.basicConfig(
    filename='logs/visualizer.log',
    level=logging.DEBUG,
    # format=f'%(levelname)s %(name)s : %(message)s')
    format=f'[%(asctime)s] %(levelname)s: %(pathname)s in line %(lineno)s: %(message)s')

app = Flask(__name__)

log = create_logger(app)

app.config.from_object("config.DevelopmentConfig")

# if app.config["ENV"] == "production":
#     app.config.from_object("config.ProductionConfig")
# else:
#     app.config.from_object("config.DevelopmentConfig")

# print(f'ENV is set to: {app.config["ENV"]}')
# print(app.config)
# basedir = os.path.abspath(os.path.dirname(__file__))
# print(basedir)

# db = SQLAlchemy(app)
# Migrate(app, db)

# csrf = CSRFProtect(app)

# login configurations
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'users.login'
# login_manager.login_message_category = 'warning'

# blueprints
from visualizer.core.views import core_blueprint
from visualizer.error_pages.handlers import error_pages

app.register_blueprint(core_blueprint)
app.register_blueprint(error_pages)