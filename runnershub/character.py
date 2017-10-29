from flask import url_for, abort
from flask_login import current_user
from flask_restful import Resource, reqparse
from flask_security.decorators import auth_token_required
from .models import PC, NPC, db


def verify_status(status):
    """
    Checks if the given status exists.
    :param status: A status to check.
    :return: None. Aborts the request if the status does not exist.
    """
    if status not in ("Active", "Retired", "Dead", "MIA", "AWOL", "Other"):
        abort(404, "Status must be one of: Active, Retired, Dead, MIA, AWOL or Other")


def check_security(user, sec_level, message):
    """
    Checks the security level of the given user against a provided level.
    :param user: User to check security level of.
    :param sec_level: Required minimum security level.
    :param message: If the request fails, the error message will be "You must have at least <sec_level> access to
    <message>"
    :return: None. Aborts the request if the user does not have permission.
    """
    if sec_level not in ("Player", "GM", "Campaign Owner", "Admin"):
        abort(400, "Security must be one of: Player, GM, Campaign Owner or Admin")

    security_int = {"Player": 0, "GM": 5, "Campaign Owner": 10, "Admin": 15}
    user_sec = max([security_int[role] for role in user.roles])
    if user_sec < security_int[sec_level]:
        abort(403, "You must have at least %s level access to %s" % (sec_level, message))


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
        check_security(current_user, npc.security, "view this NPC")

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
        check_security(current_user, npc.security, "edit this NPC")
        check_security(current_user, args['security'], "change an NPCs security to %s" % args['security'])
        if args['status'] is None:
            args['status'] = "Active"
        else:
            verify_status(args['status'])

        for item in args.keys():
            if args[item] is not None:
                setattr(npc, item, args[item])
        db.session.add(npc)
        db.session.commit()

        return {"URI": url_for("npc", id=id)}

    def delete(self, id):
        npc = NPC.query.filter_by(id=id).one_or_none()
        if npc is None:
            abort(404, "NPC does not exist")
        check_security(current_user, npc.security, "delete this NPC")

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
        check_security(current_user, args['security'], "create a new NPC with security %s" % args['security'])

        char = NPC(args['name'], args['description'], args['status'], args['security'], args['connection'])
        db.session.add(char)
        db.session.commit()
        return {"URI": url_for("npc", id=char.id)}, 201


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

        for item in args.keys():
            if args[item] is not None:
                setattr(char, item, args[item])
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
