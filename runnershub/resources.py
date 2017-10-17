from flask import url_for, abort
from flask_restful import Resource, reqparse
from .models import PC, NPC, db, User, Contact
from flask_login import current_user
from flask_security.decorators import auth_token_required
from flask_security.utils import verify_password


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
        #TODO: GMs can only edit NPCs or their own characters
        char = PC.query.filter_by(id=id).one_or_none()
        args = self.reqparse.parse_args()
        if char is None:
            abort(404, "The requested character does not exist")
        if char.owner is not current_user.id:
            abort(403, "You may only edit your own characters")
        if args['status'] is None:
            args['status'] = "Active"
        elif args['status'] not in ("Active", "Retired", "Dead", "MIA", "AWOL", "Other"):
            abort(404, "Status must be one of: Active, Retired, Dead, MIA, AWOL or Other")

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
        elif args['status'] not in ("Active", "Retired", "Dead", "MIA", "AWOL", "Other"):
            abort(404, "Status must be one of: Active, Retired, Dead, MIA, AWOL or Other")

        char = PC(args['name'], args['description'], args['status'], current_user.id, args['karma'], args['nuyen'])
        db.session.add(char)
        db.session.commit()
        return {"URI": url_for("pc", id=char.id)}, 201


class ContactAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("connection", type=int, location='json')
        self.reqparse.add_argument("loyalty", type=int, location='json')
        self.reqparse.add_argument("chips", type=int, location='json')
        super(ContactAPI, self).__init__()

    def put(self, id):
        pass

    def delete(self, id):
        pass


class ContactListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("character", type=int, required=True, location='json')
        self.reqparse.add_argument("character", type=int, required=True, location='json')
        self.reqparse.add_argument("character", type=int, required=True, location='json')
        self.reqparse.add_argument("character", type=int, required=True, location='json')
        self.reqparse.add_argument("character", type=int, required=True, location='json')


# Account stuff below
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
