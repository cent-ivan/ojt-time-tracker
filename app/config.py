'''
A centralized Configuration file of the app
'''
from datetime import timedelta
from flask import redirect, url_for
from dotenv import load_dotenv
import os

from .extensions import login_manager
from .blueprints.central_models import *

load_dotenv()

class Config():
    TESTING = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

class LoginManagerConfig():
    def config_login(login_manager):
        @login_manager.user_loader
        def load_user(user):
            #since get_id returns 'user_type-id'
            data = user.split('-')
            user_type, id = data
            if user_type == 'adviser':
                return AdviserModel.query.get(user)
            else:
                return StudentModel.query.get(user)
        
        @login_manager.unauthorized_handler  #if the user is not authorized it will redirect in this endpoint
        def unauthorized_callback():
            return redirect(url_for('auth.login'))
           