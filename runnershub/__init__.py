from flask import Flask
from .config import configure_app
from flask_restful import Api
from .resources import CharacterAPI, CharacterListAPI, db, LoginAPI

app = Flask(__name__)

api = Api(app)
configure_app(app)
db.init_app(app)

api.add_resource(CharacterAPI, '/api/character/<int:id>', endpoint='character')
api.add_resource(CharacterListAPI, '/api/characters', endpoint='characters')
api.add_resource(LoginAPI, '/api/login')
