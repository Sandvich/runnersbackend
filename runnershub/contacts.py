from flask import abort, url_for
from flask_login import current_user
from flask_restful import Resource, reqparse
from flask_security import auth_token_required
from .models import Contact, PC, NPC, db
from .character import check_security


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


class ContactCreateAPI(Resource):
    decorators = [auth_token_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("pc", type=int, required=True, location='json')
        self.reqparse.add_argument("npc", type=int, required=True, location='json')
        self.reqparse.add_argument("security", type=str, required=True, location='json')
        self.reqparse.add_argument("loyalty", type=int, required=True, location='json')
        self.reqparse.add_argument("chips", type=int, required=True, location='json')
        super(ContactCreateAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        check_security(current_user, "GM", "create a contact")
        check_security(current_user, args['security'], "create a contact with security %s" % args['security'])

        pc = PC.query.filter_by(id=args['pc']).one_or_none()
        if pc is None:
            abort(404, "Requested PC does not exist")
        npc = NPC.query.filter_by(id=args['npc']).one_or_none()
        if npc is None:
            abort(404, "Requested NPC does not exist")

        new_contact = Contact(args['pc'], args['npc'], args['loyalty'], args['chips'])
        db.session.add(new_contact)
        db.session.commit()
        return {"URI": url_for("contact", id=new_contact.id)}, 201
