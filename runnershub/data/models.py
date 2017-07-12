from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin, hash_password

db = SQLAlchemy()

class Role(db.Model, RoleMixin):
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(80), unique=True)
	description = db.Column(db.String(255))

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Role %r>' % (self.name)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(255))
	roles = db.Column(db.ForeignKey, 'Role')

	def __init__(self, email, password, roles):
		self.email = email
		self.password = hash_password(password)
		self.roles = roles
	
	def __repr__(self):
		return '<User %r>' % (self.email)
