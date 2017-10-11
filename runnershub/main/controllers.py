from flask import Blueprint, Response
import json

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return Response(json.dumps({'response':'Welcome!'}), status=200, mimetype='application/json')
