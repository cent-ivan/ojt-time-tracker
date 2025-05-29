from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Time, Boolean
from sqlalchemy import ForeignKey, orm, insert, select, update, and_, or_
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from flask_login import LoginManager, UserMixin
from flask_bcrypt import Bcrypt
import psycopg2
from psycopg2 import sql


db = SQLAlchemy()

login_manager = LoginManager()
bcrypt = Bcrypt()
