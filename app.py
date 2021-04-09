import os
from flask import Flask, request,jsonify
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from blacklist import BLACKLIST
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, UserList, UserLogin, UserLogout, VerifyJWT,TokenRefresh
from resources.tournament import Tournament, TournamentList
from resources.sport import Sport, SportList
from resources.team import TeamList,Team, TeamSports, TeamStatus,TeamDetails
from resources.player import Player, PlayerList, PlayerSports
from resources.match import Match, MatchListByTour,MatchListBySport,CompMatchListByTour,PendMatchListByTour
from resources.result import ResultTeam,ResultNet,ResultCricket

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')
#app.config["JWT_BLACKLIST_ENABLED"]=True
#app.config["JWT_BLACKLIST_TOKEN_CHECKS"]=['access','refresh']
#app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

api = Api(app)

jwt = JWTManager(app)

CORS(app)

@jwt.expired_token_loader
def expired_token_response(jwt_header, jwt_payload):
    return jsonify({
        "description":"This token has expired.",
        "error":"token_expired"
    }),401

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in BLACKLIST 


# @jwt.invalid_token_loader           THESE 3 METHODS ARE NOT REQUIRED CURRENTLY
# def invalid_token_callback(error):  
#     return jsonify({
#         'description': 'Signature verification failed.',
#         'error': 'invalid_token'
#     }), 401


# @jwt.unauthorized_loader
# def missing_token_callback(error):
#     return jsonify({
#         'description': 'Request does not contain an access token.',
#         'error': 'authorization_required'
#     }), 401


# @jwt.needs_fresh_token_loader     
# def token_not_fresh_response(jwt_header, jwt_payload):
#     return jsonify({
#         'description': 'The token is not fresh.',
#         'error': 'fresh_token_required'
#     }), 401


@jwt.revoked_token_loader
def revoked_token_response(jwt_header, jwt_payload):
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401



api.add_resource(UserRegister,"/register")
api.add_resource(UserList,"/getUsers")
api.add_resource(UserLogin,"/login")
api.add_resource(UserLogout,"/logout")
api.add_resource(TokenRefresh,"/refresh")
api.add_resource(VerifyJWT,"/verify")
api.add_resource(Tournament,"/tournament")
api.add_resource(TournamentList,"/tournamentList")
api.add_resource(Sport,"/sports")
api.add_resource(SportList,"/tournament/getSports/<int:id_>")
api.add_resource(Team,"/team")
api.add_resource(TeamDetails,"/team/<int:tid_>")
api.add_resource(Player,"/player")
api.add_resource(TeamList, "/teams/<int:id_>")
api.add_resource(PlayerList,"/tournament/playerList/<int:id_>")
api.add_resource(TeamSports, "/<int:id_>/<string:sport>/teams")
api.add_resource(PlayerSports, "/<int:id_>/<string:sport>/players")
api.add_resource(Match, "/match")
api.add_resource(MatchListBySport,"/matches/<int:id_>/<string:sport>")
api.add_resource(MatchListByTour, "/<int:id_>/matchList")
api.add_resource(CompMatchListByTour, "/<int:id_>/completedMatchList")
api.add_resource(PendMatchListByTour, "/<int:id_>/pendingMatchList")
api.add_resource(ResultTeam,"/match/team/result/<int:mid_>")
api.add_resource(ResultNet,"/match/net/result/<int:mid_>")
api.add_resource(ResultCricket,"/match/cricket/result/<int:mid_>")
api.add_resource(TeamStatus,"/team/<string:status>")

if __name__ == "__main__":
    app.run(debug = True)