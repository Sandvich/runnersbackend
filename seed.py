from runnershub import app
from runnershub.models import *
from flask_security.utils import hash_password


def create_roles(user_datastore):
    user_datastore.create_role(name="Admin", description="Site Administrator")
    user_datastore.create_role(name="Campaign Owner", description="The owner of the overall campaign, who gets the "
                                                                  "final say in plot-related things.")
    user_datastore.create_role(name="GM", description="Hub GM (may also be a player)")
    user_datastore.create_role(name="Player", description="Hub Player")
    user_datastore.commit()


def create_users(user_datastore):
    user1 = user_datastore.create_user(email="sanchitsharma1@gmail.com",
                                       password=hash_password("password"),
                                       active=True)
    user_datastore.add_role_to_user(user1, 'Admin')
    user_datastore.add_role_to_user(user1, 'GM')
    user_datastore.add_role_to_user(user1, 'Campaign Owner')

    user2 = user_datastore.create_user(email="test@test.com",
                                       password=hash_password("password"),
                                       active=True)
    user_datastore.add_role_to_user(user2, 'Player')
    user_datastore.commit()


def seed():
    user_datastore = app.security.datastore
    with app.app_context():
        db.drop_all()
        db.create_all()

        create_roles(user_datastore)
        create_users(user_datastore)


if __name__ == '__main__':
    seed()
