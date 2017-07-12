from runnershub.data.models import db, Role, User
from flask_compress import Compress
from flask_security import Security, SQLAlchemyUserDatastore
import os
import logging


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    # sqlite :memory: identifier is the default if no filepath is present
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = '1d654586-e830-431b-b21e-325744c3317b'
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'runnershub.log'
    LOGGING_LEVEL = logging.DEBUG
    SECURITY_CONFIRMABLE = False
    CACHE_TYPE = 'simple'
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', \
'application/json', 'application/javascript']
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500
    SUPPORTED_LANGUAGES = {'en': 'English'}
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'sooper-secret'


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'testing-sekrit'

config = {
    "development": "runnershub.config.DevelopmentConfig",
    "testing": "runnershub.config.TestingConfig",
    "default": "runnershub.config.DevelopmentConfig"
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)
    # Configure logging
    handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    # Configure Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore)
    # Configure Compressing
    Compress(app)
