from flask import Flask
from flask_restful import Resource, Api
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from control import *
from flask_httpauth import HTTPBasicAuth
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
from models import *

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

engine = create_engine('postgresql://postgres:1234@localhost/db1', echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


@auth.verify_password
def verify_password(username, password):
    try:
        user = session.query(User).filter(User.username == username). \
            filter(User.password == generate_password_hash(password)).one()
        return user
    except NoResultFound:
        return None
    except MultipleResultsFound:
        return None
    return None


if __name__ == "__main__":
    # event1 = Event(name="lets play!",status={"res","res","green"})
    # event2 = Event(name="fight!", status={"start", "game", "green"})
    # user=User(username="terry",firstname="ddd",lastname="ddd",password="12345")
    # session.add(event1)
    # session.add(event2)
    # session.add(user)
    # session.commit()
    api.add_resource(AddEvent, '/event/add')
    api.add_resource(UpdateEvent, '/event/update')
    api.add_resource(DeleteEvent, '/event/delete')
    api.add_resource(Test, '/test')
    api.add_resource(GetAllUserEvents, '/user/events')
    api.add_resource(SignUpUser, '/user/sign')

    api.add_resource(GetAllEvents, '/event/getall')
    app.run(debug=True)
