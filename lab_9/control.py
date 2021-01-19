from flask import Response, request, jsonify
from flask_restful import Resource

from models import *
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask import json
from werkzeug.security import generate_password_hash, check_password_hash
from app import *
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker



class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


# +
class AddEvent(Resource):
    @auth.login_required
    def post(self):
        data = request.json
        try:
            temp_event = Event(name=data["name"],status=data["status"])
            # temp_event = Event(name="hello", status={"i am groot", "great"})
            us_id = auth.current_user()
            app_db.session.add(temp_event)
            app_db.session.flush()
            relation_event = Events_User(event=temp_event, user=us_id)
            app_db.session.add(relation_event)
            app_db.session.flush()
            app_db.session.commit()
            return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            return Response(
                response=json.dumps({"message": "Invalid input"}),
                status=405,
                mimetype="application/json"
            )


# +
class UpdateEvent(Resource):
    @auth.login_required
    def put(self):
        # should write in body
        data = request.json
        if "id_event" in data:
            id_ = data['id_event']
        else:
            return Response(
                response=json.dumps({"message": "No Id !"}),
                status=404,
                mimetype="application/json"
            )
        try:
            temp = session.query(Event).get(id_)
            # if "id_event" in data:
            #     course1.name = data["id_event"]
            if "name" in data:
                temp.name = data['name']
            else:
                temp.name = "test"
            # if "status" in data:
            #     course1.status = data["status"]
            session.commit()
            return Response(
                response=json.dumps({"message": "Hurray !"}),
                status=200,
                mimetype="application/json"
            )
        except:
            return Response(
                response=json.dumps({"message": "Error !"}),
                status=500,
                mimetype="application/json"
            )


# +
class DeleteEvent(Resource):
    # @auth.login_required
    def delete(self):
        try:
            data = request.json
            id_event = data["id_event"]
            # id_event=9
            course = session.query(Event).filter(Event.id_event == id_event).first()

            if course:
                session.delete(course)
                session.commit()
                return Response(
                    response=json.dumps({"message": "It works !"}),
                    status=200,
                    mimetype="application/json"
                )
            return Response(
                response=json.dumps({"message": "Error !"}),
                status=404,
                mimetype="application/json"
            )
        except Exception as e:
            return Response(
                response=json.dumps({"message": "Error !"}),
                status=500,
                mimetype="application/json"
            )


class GetAllEvents(Resource):
    #@auth.login_required()
    def get(self):
        temp = session.query(Event).all()
        if temp:
            return Response(
                response=json.dumps(temp, cls=AlchemyEncoder),
                status=200,
                mimetype="application/json"
            )
        return Response(
            response=json.dumps({"message": "Not found"}),
            status=404,
            mimetype="application/json"
        )


class GetAllUserEvents(Resource):
    @auth.login_required
    def get(self):
        temp = auth.current_user()
        if temp.my_events:
            return Response(
                response=json.dumps(temp.my_events, cls=AlchemyEncoder),
                status=200,
                mimetype="application/json"
            )
        return Response(
            response=json.dumps({"message": "No event for user"}),
            status=404,
            mimetype="application/json"
        )


class SignUpUser(Resource):
    def post(self):
        try:
            data = request.json
            user = User(data["username"], data["firstname"], data["lastname"],
                        data["email"], data["password"])
            if session.query(User).filter(User.email == user.email).all() \
                    and session.query(User).filter(User.username == user.username).all():
                return Response(
                    response=json.dumps({"message": "user already created"}),
                    status=405,
                    mimetype="application/json"
                )
            else:
                user.password = generate_password_hash(data["password"])
                session.add(user)
                session.flush()
                session.commit()
                return Response(
                response=json.dumps({"message": "Success"}),
                status=200,
                mimetype="application/json"
            )
        except:
            return Response(
                response=json.dumps({"message": "wrong input"}),
                status=404,
                mimetype="application/json"
            )


# class Login(Resource):
#     def post(self,name,password):
#         temp = session.query(User).filter(name).get(password)
#         if


# class Test(Resource):
#     def post(self):
#         user1 = User(username="steve", firstname="jared", lastname="fief", password="123")
#         session.add(user1)
#         user2 = User(username="max", firstname="red", lastname="tagger", password="12233")
#         session.add(user2)
#         user3 = User(username="oleg", firstname="rect", lastname="aired", password="6575")
#         session.add(user3)
#         event1 = Event(name="hello", status={"i am groot", "great"})
#         session.add(event1)
#         event2 = Event(name="study", status={"read", "smile"})
#         session.add(event2)
#         event3 = Event(name="work", status={"hard", "smart"})
#         session.add(event3)
#         event3.users.append(user1)
#         event3.users.append(user2)
#         event1.users.append(user1)
#         event2.users.append(user2)
#         session.commit()
