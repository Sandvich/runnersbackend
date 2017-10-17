from flask import url_for, abort
from flask_login import current_user
from flask_restful import Resource, reqparse
from flask_security.decorators import auth_token_required, roles_required
from .models import NPC, db
from .PC import verify_status


def check_editable(editor, sec_level):
    if sec_level not in ("Player", "GM", "Campaign Owner", "Admin"):
        abort(404, "Security must be one of: Player, GM, Campaign Owner or Admin")

    security_int = {"Player": 0, "GM": 5, "Campaign Owner": 10, "Admin": 15}
    user_sec = max([security_int[role] for role in editor.roles])
    if user_sec < security_int[sec_level]:
        abort(403, "You must have at least %s level access to view or edit this resource." % sec_level)


class NPCAPI(Resource):
    decorators = [auth_token_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("name", type=str, location='json')
        self.reqparse.add_argument("description", type=str, location='json')
        self.reqparse.add_argument("status", type=str, location='json')
        self.reqparse.add_argument("security", type=str, location='json')
        self.reqparse.add_argument("connection", type=int, location='json')
        super(NPCAPI, self).__init__()

    def get(self, id):
        npc = NPC.query.filter_by(id=id).one_or_none()
        if npc is None:
            abort(404, "NPC does not exist")
        check_editable(current_user, npc.security)

        return {"name": npc.name,
                "description": npc.description,
                "status": npc.status,
                "security": npc.security,
                "connection": npc.connection}

    def put(self, id):
        npc = NPC.query.filter_by(id=id).one_or_none()
        args = self.reqparse.parse_args()
        if npc is None:
            abort(404, "The requested character does not exist")
        check_editable(current_user, npc.security)
        if args['status'] is None:
            args['status'] = "Active"
        else:
            verify_status(args['status'])

        if (args["name"] is not None) and (args["name"] != npc.name):
            npc.name = args["name"]
        if (args["description"] is not None) and (args["description"] != npc.description):
            npc.description = args["description"]
        if (args['status'] is not None) and (args['status'] != npc.status):
            npc.status = args['status']
        if (args['security'] is not None) and (args['security'] != npc.security):
            npc.security = args['security']
        if (args['connection'] is not None) and (args['connection'] != npc.connection):
            npc.connection = args['connection']

        db.session.add(npc)
        db.session.commit()

        return {"URI": url_for("npc", id=id)}

    def delete(self, id):
        npc = NPC.query.filter_by(id=id).one_or_none()
        if npc is None:
            abort(404, "NPC does not exist")
        check_editable(current_user, npc.security)

        db.session.delete(npc)
        db.session.commit()
        return {"message": "Success"}


class NPCListAPI(Resource):
    decorators = [auth_token_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("name", required=True, type=str, location='json')
        self.reqparse.add_argument("description", required=True, type=str, location='json')
        self.reqparse.add_argument("status", required=True, type=str, location='json')
        self.reqparse.add_argument("security", required=True, type=str, location='json')
        self.reqparse.add_argument("connection", required=True, type=int, location='json')
        super(NPCListAPI, self).__init__()

    def get(self):
        allchars = NPC.query.all()
        return [{"name": char.name, "URI": url_for("npc", id=char.id)} for char in allchars]

    def post(self):
        args = self.reqparse.parse_args()
        if args['status'] is None:
            args['status'] = "Active"
        else:
            verify_status(args['status'])
        check_editable(current_user, args['security'])

        char = NPC(args['name'], args['description'], args['status'], args['security'], args['connection'])
        db.session.add(char)
        db.session.commit()
        return {"URI": url_for("npc", id=char.id)}, 201
