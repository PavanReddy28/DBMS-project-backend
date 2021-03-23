import psycopg2
import os
from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_bcrypt import check_password_hash, generate_password_hash

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="username cant be blank"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="password cannot be blank"
                        )

    def post(self):

        data = UserRegister.parser.parse_args()

        user = UserModel.find_by_name(data['username'])
        if user:
            return {
                "message":"user already exists"
            }
        else:
            hash_ = generate_password_hash(data['password']).decode('utf-8')
            user = UserModel(data['username'],hash_)
            user.save_to_db()

        return {
            "message":"user with {} added".format(data["username"])
        }

    
class UserList(Resource):
    def get(self):
        userList = {
            "users": []
        }

        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("SELECT * FROM users")

        result = cur.fetchall()

        conn.close()

        for row in result:
            userList['users'].append({
                "username": row[0],
                "hashed password": row[1]
                })
        
        conn.close()

        return userList
    

class UserLogin(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="username cant be blank"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="password cannot be blank"
                        )

    def post(self):
        data = UserLogin.parser.parse_args()

        user = UserModel.find_by_name(data['username'])
        
        if user:
            print(user.password)
            if check_password_hash(user.password,data['password']):
                access_token = create_access_token(identity= user.username,fresh=True)
                refresh_token = create_refresh_token(user.username)
            
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }, 200
            else:
                return {
                    "message": "wrong password"
                },401
        else:
            return {
                "message": "username not found"
            },401