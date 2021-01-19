from flask_sqlalchemy import SQLAlchemy

from app import *
import unittest
from flask_fixtures import FixturesMixin

from config_test import Test_Config


class SignupTest(unittest.TestCase, FixturesMixin):
    fixtures = ['users.json']
    app=app
    db = SQLAlchemy(app)

    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
        # self.db = engine.get_db()

    def test_get_all_events(self):
        response = self.app.get('/event/getall', headers={"Authorization": "Basic bWF4OjEyMjMz"})

        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.json))

    # def tearDown(self):
    #     for collection in self.db.list_collection_names():
    #         self.db.drop_collection(collection)


if __name__ == '__main__':
    unittest.main()
