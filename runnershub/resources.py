from flask import url_for, abort
from flask_restful import Resource, reqparse
from .models import Character, db, User
from flask_login import current_user
from flask_security.decorators import auth_token_required
from flask_security.utils import verify_password


class CharacterAPI(Resource):
    decorators = [auth_token_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("name", type=str, location='json')
        self.reqparse.add_argument("description", type=str, location='json')
        self.reqparse.add_argument("pc", type=bool, location='json')
        super(CharacterAPI, self).__init__()

    def get(self, id):
        char = Character.query.filter_by(id=id).one_or_none()
        if char is None:
            abort(404, "The requested character does not exist")

        return {"name": char.name, "description": char.description, "pc": char.pc, "URI": url_for("character", id=id)}

    def put(self, id):
        char = Character.query.filter_by(id=id).one_or_none()
        if char is None:
            abort(404, "The requested character does not exist")

        args = self.reqparse.parse_args()

        changed = []
        if (args["name"] is not None) and (args["name"] != char.name):
            char.name = args["name"]
            changed.append("name")
        if (args["description"] is not None) and (args["description"] != char.description):
            char.description = args["description"]
            changed.append("description")
        if (args["pc"] is not None) and (args["pc"] != char.pc):
            char.pc = args["pc"]
            changed.append("pc")

        if len(changed) > 0:
            db.session.add(char)
            db.session.commit()

        return {"changed": changed, "URI": url_for("character", id=id)}

    def delete(self, id):
        char = Character.query.filter_by(id=id).one_or_none()
        if char is None:
            abort(404, "The requested character does not exist")
        db.session.delete(char)
        db.session.commit()
        return {"status": "Success"}


class CharacterListAPI(Resource):
    decorators = [auth_token_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("name", type=str, required=True, help="Character name is required", location='json')
        self.reqparse.add_argument("description", type=str, required=True, help="Description required.", location='json')
        self.reqparse.add_argument("pc", type=bool, required=True, help="Please set to True if character is a PC",
                                   location='json')
        super(CharacterListAPI, self).__init__()

    def get(self):
        allchars = Character.query.all()
        return [{"name": char.name, "URI": url_for("character", id=char.id)} for char in allchars]

    def post(self):
        args = self.reqparse.parse_args()
        char = Character(args['name'], args['description'], args['pc'], current_user.id)
        db.session.add(char)
        db.session.commit()
        return {"URI": url_for("character", id=char.id)}, 201


class LoginAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("email", type=str, required=True, help="Email required!", location='json')
        self.reqparse.add_argument("password", type=str, required=True, help="Password required!", location='json')
        super(LoginAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        user = User.query.filter_by(email=args["email"]).one_or_none()
        if user is None:
            abort(403, "User not found")
        if verify_password(args["password"], user.password):
            return {"auth": user.get_auth_token()}
        else:
            abort(403, "Wrong password")
