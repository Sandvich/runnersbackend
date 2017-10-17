from flask import url_for, abort
from flask_login import current_user
from flask_restful import Resource, reqparse
from flask_security.decorators import auth_token_required
from .models import PC, db


def verify_status(status):
    if status not in ("Active", "Retired", "Dead", "MIA", "AWOL", "Other"):
        abort(404, "Status must be one of: Active, Retired, Dead, MIA, AWOL or Other")


class PCAPI(Resource):
    decorators = [auth_token_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("name", type=str, location='json')
        self.reqparse.add_argument("description", type=str, location='json')
        self.reqparse.add_argument("status", type=str, location='json')
        self.reqparse.add_argument("karma", type=int, location='json')
        self.reqparse.add_argument("nuyen", type=int, location='json')
        super(PCAPI, self).__init__()

    def get(self, id):
        char = PC.query.filter_by(id=id).one_or_none()
        if char is None:
            abort(404, "The requested character does not exist")

        return {"name": char.name,
                "description": char.description,
                "URI": url_for("pc", id=id),
                "status": char.status,
                "karma": char.karma,
                "nuyen": char.nuyen}

    def put(self, id):
        char = PC.query.filter_by(id=id).one_or_none()
        args = self.reqparse.parse_args()
        if char is None:
            abort(404, "The requested character does not exist")
        if char.owner is not current_user.id:
            abort(403, "You may only edit your own characters")
        if args['status'] is None:
            args['status'] = "Active"
        else:
            verify_status(args['status'])

        if (args["name"] is not None) and (args["name"] != char.name):
            char.name = args["name"]
        if (args["description"] is not None) and (args["description"] != char.description):
            char.description = args["description"]
        if (args['status'] is not None) and (args['status'] != char.status):
            char.status = args['status']
        if (args['karma'] is not None) and (args['karma'] != char.karma):
            char.karma = args['karma']
        if (args['nuyen'] is not None) and (args['nuyen'] != char.nuyen):
            char.nuyen = args['nuyen']

        db.session.add(char)
        db.session.commit()

        return {"URI": url_for("pc", id=id)}

    def delete(self, id):
        char = PC.query.filter_by(id=id).one_or_none()
        if char is None:
            abort(404, "The requested character does not exist")
        if char.owner is not current_user.id:
            if current_user.has_role("Player") and not current_user.has_role("GM"):
                abort(403, "You may only delete your own characters")

        db.session.delete(char)
        db.session.commit()
        return {"message": "Success"}


class PCListAPI(Resource):
    decorators = [auth_token_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("name", type=str, required=True, help="Character name is required", location='json')
        self.reqparse.add_argument("description", type=str, required=True, help="Description required", location='json')
        self.reqparse.add_argument("status", type=str, location='json')
        self.reqparse.add_argument("karma", type=int, required=True, help="Karma level is required", location='json')
        self.reqparse.add_argument("nuyen", type=int, required=True, help="Nuyen is required", location='json')
        super(PCListAPI, self).__init__()

    def get(self):
        allchars = PC.query.all()
        return [{"name": char.name, "URI": url_for("pc", id=char.id)} for char in allchars]

    def post(self):
        args = self.reqparse.parse_args()
        if (current_user.has_role("Player")) and\
                (not current_user.has_role("GM")) and\
                (args["status"] in (None, "Active")):
            if len(PC.query.filter_by(owner=current_user.id, status="Active").all()) > 0:
                abort(403, "Players may only make one active character")
        if args['status'] is None:
            args['status'] = "Active"
        else:
            verify_status(args['status'])

        char = PC(args['name'], args['description'], args['status'], current_user.id, args['karma'], args['nuyen'])
        db.session.add(char)
        db.session.commit()
        return {"URI": url_for("pc", id=char.id)}, 201
