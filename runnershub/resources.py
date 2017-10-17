from flask import abort
from flask_restful import Resource, reqparse
from flask_security.utils import verify_password
from .models import User


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
