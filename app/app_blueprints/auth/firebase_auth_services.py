import firebase_admin
from firebase_admin import credentials, auth
from dotenv import load_dotenv
import os

load_dotenv()


class FirebaseAuth:
  
    cred = credentials.Certificate('firebase-sdk.json')
    firebase_admin.initialize_app(cred)

    def register_to_firebase_auth(email, password) -> str:
        try:
            user = auth.create_user(email=email, password=password)
            return user.uid
        except auth.EmailAlreadyExistsError as err:
            return "Exists"

    

