from flask import Flask
from .config import configure_app
from flask_restful import Api
from .resources import LoginAPI
from .PC import PCAPI, PCListAPI
from .NPC import NPCAPI, NPCListAPI
from .models import db

app = Flask(__name__)

api = Api(app)
configure_app(app)
db.init_app(app)

api.add_resource(PCAPI, '/api/pc/<int:id>', endpoint='pc')
api.add_resource(PCListAPI, '/api/pcs', endpoint='pcs')
api.add_resource(NPCAPI, '/api/npc/<int:id>', endpoint='npc')
api.add_resource(NPCListAPI, '/api/npcs', endpoint='npcs')
api.add_resource(LoginAPI, '/api/login')
