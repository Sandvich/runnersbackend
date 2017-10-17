from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()


class NPC(db.Model):
    """To be used for storing NPCs - security is who can edit the NPC, using the defined Roles"""
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.Text(convert_unicode=True))
    status = db.Column(db.String(7))
    security = db.Column(db.Integer, db.ForeignKey("role.id"))
    connection = db.Column(db.Integer(), nullable=False)

    def __init__(self, name, description, status, security, connection):
        self.name = name
        self.description = description
        self.status = status
        self.security = security
        self.connection = connection
        super(NPC, self).__init__()

    def __repr__(self):
        return '<NPC: %r editable by %r>' % (self.name, self.security)


class PC(db.Model):
    """To be used for storing PCs - can only be edited by their owners"""
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.Text(convert_unicode=True))
    status = db.Column(db.String(7))
    owner = db.Column(db.Integer, db.ForeignKey("user.id"))
    karma = db.Column(db.Integer(), nullable=False)
    nuyen = db.Column(db.Integer(), nullable=False)

    def __init__(self, name, description, status, owner, karma, nuyen):
        self.name = name
        self.description = description
        self.status = status
        self.owner = owner
        self.karma = karma
        self.nuyen = nuyen
        super(PC, self).__init__()

    def __repr__(self):
        return '<PC: %r Status: %r>' % (self.name, self.status)


class Contact(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    character = db.Column(db.Integer, db.ForeignKey("PC.id"), nullable=False)
    contact = db.Column(db.Integer, db.ForeignKey("NPC.id"), nullable=False)
    connection = db.Column(db.Integer())
    loyalty = db.Column(db.Integer())
    chips = db.Column(db.Integer())

    def __init__(self, character, contact, connection=1, loyalty=1, chips=0):
        self.character = character
        self.contact = contact
        self.connection = connection
        self.loyalty = loyalty
        self.chips = chips
        super(Contact, self).__init__()

    def __repr__(self):
        return '<Contact %r and %r>' % (PC.query.filter_by(id=self.character.id).one().name,
                                        NPC.query.filter_by(id=self.contact.id).one().name)


# Account stuff below
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name, description):
        self.name = name
        self.description = description
        super(Role, self).__init__()

    def __repr__(self):
        return '<Role %r>' % self.name


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
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
        super(User, self).__init__()

    def __repr__(self):
        return '<User %r Roles: %r>' % (self.email, self.roles)
