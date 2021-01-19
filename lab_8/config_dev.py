from config import Config


class Dev_Config(Config):
    DB_URI="postgresql://postgres:1234@localhost/db1"