import os
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, UserList, UserLogin, VerifyJWT
from resources.tournament import Tournament, TournamentList
from resources.sport import Sport, SportList
from resources.team import Team
from resources.player import Player

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')

api = Api(app)

jwt = JWTManager(app)

CORS(app)

api.add_resource(UserRegister,"/register")
api.add_resource(UserList,"/getUsers")
api.add_resource(UserLogin,"/login")
api.add_resource(VerifyJWT,"/verify")
api.add_resource(Tournament,"/tournament")
api.add_resource(TournamentList,"/tournamentList")
api.add_resource(Sport,"/sports")
api.add_resource(SportList,"/tournament/getSports")
api.add_resource(TeamRegister,"/team")
api.add_resource(PlayerRegister,"/team/player")

if __name__ == "__main__":
    app.run(debug = True)