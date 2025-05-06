#here you can do generate jwt user id, hash password
from ....extensions import bcrypt


class Generators():
    @staticmethod
    def generate_hash(password) -> str:
        return bcrypt.generate_password_hash(password).decode('utf-8')
    

    @staticmethod
    def generate_uid(type, number) -> str:
        number += 1
        uid = f"{type}-OTA:{number}"
        return uid
        