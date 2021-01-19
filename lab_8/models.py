from datetime import timedelta

from sqlalchemy import create_engine, Column, Integer, String, ARRAY, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from flask_jwt_extended import create_access_token

from werkzeug.security import check_password_hash, generate_password_hash

Base = declarative_base()
events_users = Table('events_users', Base.metadata,
                     Column('user_id', Integer, ForeignKey('users.id')),
                     Column('event_id', Integer, ForeignKey('events.id_event'))
                     )


class User(Base):
    __tablename__ = "users"

    id = Column('id', Integer, primary_key=True)
    username = Column('username', String)
    firstname = Column('firstname', String)
    lastname = Column('lastname', String)
    email = Column('email', String)
    password = Column('password', String)
    phone = Column('phone', String)
    role=Column('role', String)
    my_events = relationship("Event", secondary=events_users,cascade="all,delete")

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


class Event(Base):
    __tablename__ = "events"

    id_event = Column('id_event', Integer, primary_key=True)
    name = Column('name', String)
    status = Column('status', ARRAY(String))
    users = relationship("User", secondary=events_users,cascade="all,delete")

    def __init__(self, name, status):
        self.name = name
        self.status = status
