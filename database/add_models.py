from models import Session, User, Event, Event_Users

session1 = Session()

user1 = User(id = 1, username = "Vasya", firstname = "Pavlo", lastname = "Putin", email = "putin@gmail.com", password = "12341", phone = "0934738481", userstatus = 1)


event1 = Event(id_event = 1, name = "morgenshtern", status = "private" )
event2 = Event(id_event = 2, name = "gana", status = "public" )
event_users1 = Event_Users(id_event_user = 1, events = [1,2,3],users = [1,2,3], access = "yes" )

session1.add(user1)
session1.add(event1)
session1.add(event2)
session1.add(event_users1)


session1.commit()

session1.close()