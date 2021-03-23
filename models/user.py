from flask_bcrypt import generate_password_hash,check_password_hash

class UserModel:
    def __init__(self,username,password):
        self.username = username
        self.password = password

    def save_to_db(self):
        pass

    @classmethod
    def find_user():
        pass