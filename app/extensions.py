from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Time
from sqlalchemy import ForeignKey, orm, insert, select
from flask_migrate import Migrate

from flask_login import LoginManager, UserMixin
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
bcrypt = Bcrypt()