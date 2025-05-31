from dotenv import load_dotenv
import os
load_dotenv()


#psycopg2 config
class PostgresDatabaseConfig():
    def __init__(self):
        self.HOST = os.getenv('HOST')
        self.USER = os.getenv('DB_USER')
        self.PASSWORD = os.getenv('PASSWORD')
        self.PORT = os.getenv('PORT')
        self.DATABASE_NAME = os.getenv('DATABASE_NAME')

    #since psycopg2.connect accept keyword arguments, then you can use **.
    def return_dict(self) -> dict:
        return {
            'host' : self.HOST,
            'dbname' : self.DATABASE_NAME,
            'user' : self.USER,
            'password' : self.PASSWORD,
            'port' : self.PORT
        }