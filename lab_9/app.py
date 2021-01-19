from flask import Flask
from flask_restful import Resource, Api

from datetime import timedelta
from flask_jwt_extended import create_access_token
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import check_password_hash, generate_password_hash
from config_dev import Dev_Config
from config_test import Test_Config
from flask_httpauth import HTTPBasicAuth
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

app = Flask(__name__)
if app.env=="development":
    app.config.from_object(Dev_Config())
else:
    app.config.from_object(Test_Config())


api = Api(app)
auth = HTTPBasicAuth()

from models import *
app_db.create_all()
session = app_db.session

@auth.get_user_roles
def get_user_roles(user):
    return user.role

@auth.verify_password
def verify_password(username, password):
    try:
        user = session.query(User).filter(User.username == username).one()
        if check_password_hash(user.password,password):
            return user
    except NoResultFound:
        return None
    except MultipleResultsFound:
        return None
    return None


if __name__ == "__main__" or __name__ == "app":
    from control import *
    api.add_resource(AddEvent, '/event/add')
    api.add_resource(UpdateEvent, '/event/update')
    api.add_resource(DeleteEvent, '/event/delete')
    #api.add_resource(Test, '/test')
    api.add_resource(GetAllUserEvents, '/user/events')
    api.add_resource(GetAllEvents, '/event/getall')
    api.add_resource(SignUpUser, '/user/sign')





