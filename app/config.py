'''
A centralized Configuration file of the app
'''
from datetime import timedelta
from flask import redirect, url_for
from dotenv import load_dotenv
import os


from .blueprints.central_models import *


load_dotenv()

class Config():
    TESTING = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI') 
    SECRET_KEY = os.getenv('SECRET_KEY')
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

class LoginManagerConfig():
    @staticmethod
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
            return redirect(url_for('auth.logout'))


#psycopg2 config
class PostgresDatabaseConfig():
    def __init__(self):
        self.HOST = os.getenv('HOST')
        self.USER = os.getenv('USER')
        self.PASSWORD = os.getenv('PASSWORD')
        self.PORT = os.getenv('PORT')
        self.DATABASE_NAME = os.getenv('DATABASE_NAME')

    #since psycopg2.connect accept keyword arguments, then you can use **.
    @staticmethod
    def return_dict(self) -> dict:
        return {
            'host' : self.HOST,
            'dbname' : self.DATABASE_NAME,
            'user' : self.USER,
            'password' : self.PASSWORD,
            'port' : self.port
        }
    


           