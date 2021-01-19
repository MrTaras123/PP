from datetime import timedelta
from flask_jwt_extended import create_access_token
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import check_password_hash, generate_password_hash


from app import app
app_db=SQLAlchemy(app)

class Events_User(app_db.Model):
    __tablename__ = "events_users"

    id=app_db.Column('id', app_db.Integer, primary_key=True, autoincrement=True, unique=True)
    user_id=app_db.Column('user_id', app_db.Integer, app_db.ForeignKey('users.id'),  nullable=True)
    event_id=app_db.Column('event_id', app_db.Integer, app_db.ForeignKey('events.id_event'),  nullable=True)
    event = app_db.relationship("Event", back_populates="users")
    user = app_db.relationship("User", back_populates="my_events")


class User(app_db.Model):
    __tablename__ = "users"

    id = app_db.Column('id', app_db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = app_db.Column('username', app_db.String, nullable=False)
    firstname = app_db.Column('firstname', app_db.String)
    lastname = app_db.Column('lastname', app_db.String)
    email = app_db.Column('email', app_db.String)
    password = app_db.Column('password', app_db.String)
    phone = app_db.Column('phone', app_db.String)
    role=app_db.Column('role', app_db.String)
    my_events = app_db.relationship("Events_User", back_populates="user")

    # def __init__(self, username, firstname=None, lastname=None,
    #              email=None, password=None, phone=None,id=None,role="user"):
    #     self.id = id
    #     self.username = username
    #     self.first_name = firstname
    #     self.last_name = lastname
    #     self.email = email
    #     self.password = generate_password_hash(password)
    #     self.phone = phone
    #     self.role=role


class Event(app_db.Model):
    __tablename__ = "events"

    id_event = app_db.Column('id_event', app_db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = app_db.Column('name', app_db.String)
    status = app_db.Column('status', app_db.ARRAY(app_db.String))
    users = app_db.relationship("Events_User", back_populates="event", cascade = "all,delete")

    # def __init__(self, name, status):
    #     self.name = name
    #     self.status = status
