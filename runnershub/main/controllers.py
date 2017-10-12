from flask import Blueprint, jsonify

main = Blueprint('main', __name__)


@main.route('/', methods=["GET"])
def index():
    print("Hello")
    return jsonify({'response': 'Welcome!'})
