from flask import Flask
from runnershub.main.controllers import main
from runnershub.admin.controllers import admin
from runnershub.config import configure_app
from runnershub.data.models import db, User, Role

app = Flask(__name__)

configure_app(app)
db.init_app(app)

app.register_blueprint(main, url_prefix='/')
app.register_blueprint(admin, url_prefix='/admin')
