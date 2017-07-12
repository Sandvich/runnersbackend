from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

class Role(db.Model, RoleMixin):
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(80), unique=True)
	description = db.Column(db.String(255))

	def __init__(self, name, description):
		self.name = name
		self.description = description

	def __repr__(self):
		return '<Role %r>' % (self.name)

roles_users = db.Table('roles_users', \
db.Column('user_id', db.Integer(), db.ForeignKey('user.id')), \
db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(255))
	roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
	active = db.Column(db.Boolean())

	def __init__(self, email, password, roles, active):
		self.email = email
		self.password = password
		self.roles = roles
		self.active = active

	def __repr__(self):
		return '<User %r>' % (self.email)
