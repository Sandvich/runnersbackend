from flask import abort, url_for
from flask_login import current_user
from flask_restful import Resource, reqparse
from flask_security import auth_token_required
from .models import Contact, PC, NPC, db
from .character import check_security


class ContactAPI(Resource):
    decorators = [auth_token_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("security", type=str, location='json')
        self.reqparse.add_argument("loyalty", type=int, location='json')
        self.reqparse.add_argument("chips", type=int, location='json')
        super(ContactAPI, self).__init__()

    def put(self, id):
        contact = Contact.query.filter_by(id=id).one_or_none()
        args = self.reqparse.parse_args()
        if contact is None:
            abort(404, "The requested contact does not exist")
        check_security(current_user, contact.security, "edit this contact")
        check_security(current_user, args['security'], "change a contact's security to %s" % args['security'])

        for item in args.keys():
            if args[item] is not None:
                setattr(contact, item, args[item])
        db.session.add(contact)
        db.session.commit()

        return {"URI": url_for("contact", id=id)}

    def delete(self, id):
        contact = Contact.query.filter_by(id=id).one_or_none()
        if contact is None:
            abort(404, "Requested contact does not exist!")
        check_security(current_user, contact.security, "edit this contact")

        db.session.delete(contact)
        db.session.commit()
        return {"message": "Success"}


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
