import os
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')

api = Api(app)

jwt = JWTManager(app)

CORS(app)

if __name__ == "__main__":
    app.run(debug = True)