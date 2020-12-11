from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine("postgresql://postgres:11111@localhost/eventdb", echo = True)


Session = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column('id',Integer,primary_key=True)
    username = Column('username',String)
    firstname = Column('firstname',String)
    lastname = Column('lastname',String)
    email = Column('email',String)
    password = Column('password',String)
    phone = Column('phone',String)
    userstatus = Column('userstatus',Integer)
   

class Event(Base):
    __tablename__ = "events"

    id_event = Column('id_event',Integer,primary_key=True)
    name = Column('name',String)
    status = Column('status',ARRAY(String))


class Event_Users(Base):
    __tablename__ =  "event_user"
    id_event_user = Column('id_event_user',Integer,primary_key=True)
    events = Column('events',ARRAY(Integer))
    users = Column('users',ARRAY(Integer))
    access =  Column('access',String)