from flask_restful import Resource, reqparse
from .models import Character, db


class CharacterAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("name", type=str, required=True, location='json')
        self.reqparse.add_argument("description", type=str, location='json')
        super(CharacterAPI, self).__init__()

    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass


class CharacterListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("name", type=str, required=True, help="Character name is required", location='json')
        self.reqparse.add_argument("description", type=str, required=True, help="Description required.", location='json')
        self.reqparse.add_argument("pc", type=bool, required=True, help="Please set to True if character is a PC",
                                   location='json')
        super(CharacterListAPI, self).__init__()

    def get(self):
        allchars = Character.query.all()
        return [{"name": char.name, "description": char.description, "PC": char.pc, "ID": char.id} for char in allchars]

    def post(self):
        args = self.reqparse.parse_args()
        char = Character(args['name'], args['description'], args['pc'])
        db.session.add(char)
        db.session.commit()
        return {"name": char.name, "description": char.description, "PC": char.pc, "ID": char.id}
