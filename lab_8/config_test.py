from config import Config


class Test_Config(Config):
    SQLALCHEMY_DATABASE_URI ="postgresql://postgres:1234@localhost/test_db"
    #some uri      !!!!!!!!!
    DB_URI="postgresql://postgres:1234@localhost/test_db"