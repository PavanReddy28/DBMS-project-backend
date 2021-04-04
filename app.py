import os
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, UserList, UserLogin, VerifyJWT
from resources.tournament import Tournament, TournamentList
from resources.sport import Sport, SportList
from resources.team import TeamList,Team, TeamSports, TeamStatus
from resources.player import Player, PlayerList, PlayerSports
from resources.match import Match, MatchList
from resources.result import ResultTeam,ResultNet,ResultCricket

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
api.add_resource(Team,"/team")
api.add_resource(Player,"/player")
api.add_resource(TeamList, "/teams/<int:id_>")
api.add_resource(PlayerList,"/tournament/playerList")
api.add_resource(TeamSports, "/sport/teams")
api.add_resource(PlayerSports, "/sport/players")
api.add_resource(Match, "/match")
api.add_resource(MatchList, "/tournament/matchList")
api.add_resource(ResultTeam,"/match/team/result")
api.add_resource(ResultNet,"/match/net/result")
api.add_resource(ResultCricket,"/match/cricket/result")
api.add_resource(TeamStatus,"/team/<string:status>")

if __name__ == "__main__":
    app.run(debug = True)