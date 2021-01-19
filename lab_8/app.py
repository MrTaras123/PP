from flask import Flask
from flask_restful import Resource, Api
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import coverage
from models import *
from flask_httpauth import HTTPBasicAuth
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

engine = create_engine("postgresql://postgres:1234@localhost/db1", echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

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


if __name__ == "__main__" :
    from control import *
    api.add_resource(AddEvent, '/event/add')
    api.add_resource(UpdateEvent, '/event/update')
    api.add_resource(DeleteEvent, '/event/delete')
    api.add_resource(Test, '/test')
    api.add_resource(GetAllUserEvents, '/user/events')
    api.add_resource(GetAllEvents, '/event/getall')
    api.add_resource(SignUpUser, '/user/sign')
    app.run(debug=True)




