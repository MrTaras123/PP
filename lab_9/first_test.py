from flask_sqlalchemy import SQLAlchemy

from app import *
from control import AlchemyEncoder
from models import *
from flask import json
import unittest
from flask_fixtures import FixturesMixin

from config_test import Test_Config


class SignupTest(unittest.TestCase, FixturesMixin):
    fixtures = ['users.json', 'events.json', 'events_users.json']
    app=app
    db=app_db

    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
        app_db.engine.execute("SELECT setval('users_id_seq', (SELECT MAX(id) FROM users)+1)")
        app_db.engine.execute("SELECT setval('events_id_event_seq', (SELECT MAX(id_event) FROM events)+1)")
        app_db.engine.execute("SELECT setval('events_users_id_seq', (SELECT MAX(id) FROM events_users)+1)")
        # self.db = engine.get_db()

    def test_get_all_events(self):
        response = self.app.get('/event/getall', headers={"Authorization": "Basic bWF4OjEyMjMz"})

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json))

    def test_get_user_events(self):
        response = self.app.get('/user/events', headers={"Authorization": "Basic c3RldmU6MTIz"})

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json))

    def test_add_events(self):
        response = self.app.post('/event/add', headers={"Authorization": "Basic c3RldmU6MTIz"}, json=json.loads(json.dumps(
            Event(name="work", status={"hard", "smart"}), cls=AlchemyEncoder
        )))

        self.assertEqual(200, response.status_code)
        #TODO: check in db
        self.assertEqual(1, len(response.json))
        #-------------------------------------------
        response = self.app.post('/event/add', headers={"Authorization": "Basic c3RldmU6MTIz"},
                                 json=json.loads(json.dumps(
                                     Event(name="work", status={"hard", "smart"}), cls=AlchemyEncoder
                                 )))

        self.assertEqual(200, response.status_code)
        # TODO: check in db
        self.assertEqual(1, len(response.json))

    def test_update_event(self):
        response = self.app.put('/event/update', headers={"Authorization": "Basic c3RldmU6MTIz"}, json=json.loads(json.dumps(
            Event(name="work", status={"hard1", "smart"}), cls=AlchemyEncoder
        )))

        self.assertEqual(500, response.status_code)
        #TODO: check in db
        self.assertEqual(1, len(response.json))

        response = self.app.put('/event/update', headers={"Authorization": "Basic c3RldmU6MTIz"}, json=json.loads(json.dumps(
            Event(name="work", id_event=1, status={"hard1", "smart"}), cls=AlchemyEncoder
        )))

        self.assertEqual(200, response.status_code)
        #TODO: check in db
        self.assertEqual(1, len(response.json))

    def test_delete_event(self):
        response = self.app.delete('/event/delete', headers={"Authorization": "Basic c3RldmU6MTIz"}, json=json.loads(json.dumps(
            Event(id_event=1), cls=AlchemyEncoder
        )))

        self.assertEqual(200, response.status_code)
        #TODO: check in db
        self.assertEqual(1, len(response.json))

        response = self.app.delete('/event/delete', headers={"Authorization": "Basic c3RldmU6MTIz"}, json=json.loads(json.dumps(
            Event(id_event=100), cls=AlchemyEncoder
        )))

        self.assertEqual(404, response.status_code)
        #TODO: check in db
        self.assertEqual(1, len(response.json))

    def test_sign_up(self):
        response = self.app.post('/user/sign', headers={"Authorization": "Basic c3RldmU6MTIz"},
                                 json=json.loads(json.dumps(
                                     User(username="username", firstname="firstname",lastname="lastname",
                                          email="email",password="password"
                                          ), cls=AlchemyEncoder
                                 )))

        self.assertEqual(404, response.status_code)
        self.assertEqual(1, len(response.json))

    def tearDown(self):
        app_db.session.remove()
        app_db.drop_all()
  

if __name__ == '__main__':
    unittest.main()
