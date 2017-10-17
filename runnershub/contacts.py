from flask import abort
from flask_restful import Resource, reqparse
from .models import Contact


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