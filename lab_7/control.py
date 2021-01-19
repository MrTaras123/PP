from flask import Response, request, jsonify
from flask_restful import Resource

from app import session
from models import *
from flask import json

from app import *
from sqlalchemy.ext.declarative import DeclarativeMeta


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



class AddEvent(Resource):
    # @auth.login_required
    def post(self):
        data = request.json
        try:
            temp_event = Event(data["name"], data["status"])
            # temp_event = Event(name="hello", status={"i am groot", "great"})
            us_id = data["id_"]
            session.add(temp_event)
            temp_user = session.query(User).get(us_id)
            temp_event.users.append(temp_user)
            temp_user.my_events.append(temp_event)

            session.flush()
            session.commit()
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



class UpdateEvent(Resource):
    # @auth.login_required
    def put(self):
        data = request.json
        if session.query(Event).get(data["id_"]) == None:
            return Response(
                response=json.dumps({"message": "No Id !"}),
                status=404,
                mimetype="application/json"
            )
        try:
            temp = session.query(Event).get(data["id_"])

            temp.name = data["name"]

            session.commit()
            return Response(
                response=json.dumps({"message": "Hurray !"}),
                status=200,
                mimetype="application/json"
            )
        except Exception as e:
            return Response(
                response=json.dumps({"message": "Error !"}),
                status=405,
                mimetype="application/json"
            )



class DeleteEvent(Resource):
    @auth.login_required
    def delete(self):
        try:
            data = request.json
            id_event = data["id_event"]
            # id_event=9
            course = session.query(Event).get(id_event)
            session.delete(course)
            session.commit()
            if course:
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
        except:
            return Response(
            response=json.dumps({"message": "Error !"}),
            status=404,
            mimetype="application/json"
        )



class GetAllEvents(Resource):
    # @auth.login_required
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
    # @auth.login_required
    def get(self):
        data = request.json
        try:
            temp = session.query(User).get(data["id"])
            if temp.my_events:
                return Response(
                    response=json.dumps(temp.my_events, cls=AlchemyEncoder),
                    status=200,
                    mimetype="application/json"
                )
            return Response(
                response=json.dumps({"message": "No event for user"}),
                status=405,
                mimetype="application/json"
            )
        except Exception as e:
            return Response(
            response=json.dumps({"message": "Error !"}),
            status=404,
            mimetype="application/json"
        )


class Test(Resource):
    def post(self):
        user1 = User(username="steve",  password="123")
        session.add(user1)
        user2 = User(username="max",password="12233")
        session.add(user2)
        user3 = User(username="oleg", password="6575")
        session.add(user3)
        event1 = Event(name="steve", status={"fly", "dream"})
        session.add(event1)
        event2 = Event(name="study", status={"read", "smile"})
        session.add(event2)
        event3 = Event(name="work", status={"hard", "smart"})
        session.add(event3)
        event3.users.append(user1)
        event3.users.append(user2)
        event1.users.append(user1)
        event2.users.append(user2)
        session.commit()


class SignUpUser(Resource):
    def post(self):
        data = request.json
        try:
            #user = User(data["username"], data["firstname"], data["lastname"],
                        #data["email"], data["password"])
            user = User(data["username"], data["password"])
            if session.query(User).filter(User.email == user.email).all() \
                    and session.query(User).filter(User.username == user.username).all():
                return Response(
                    response=json.dumps({"message": "user already created"}),
                    status=405,
                    mimetype="application/json"
                )
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
