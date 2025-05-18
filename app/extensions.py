from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Time, Boolean
from sqlalchemy import ForeignKey, orm, insert, select, update, and_, or_
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin
from flask_bcrypt import Bcrypt
import psycopg2
from psycopg2 import sql


db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
bcrypt = Bcrypt()

class PostgresDatabase():
    #for psycopg2 config
    def __init__(self, **params):
        self.host = params["host"]
        self.default_db = params["default_db"]
        self.user = params["user"]
        self.password = params["password"]
        self.port = params["port"]
        self.database = params["database"]