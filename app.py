import os
from datetime import timedelta
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
from resources.match import Match, MatchListByTour,MatchListBySport,CompMatchListByTour,PendMatchListByTour,CompMatchListBySport,PendMatchListBySport
from resources.result import ResultTeam,ResultNet,ResultCricket,ResultListBySport,ResultListByTourn

ACCESS_EXPIRES = timedelta(hours=1)

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')
#app.config["JWT_BLACKLIST_ENABLED"]=True
#app.config["JWT_BLACKLIST_TOKEN_CHECKS"]=['access','refresh']
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

api = Api(app)

@app.before_first_request
def init_db():
    url = url = os.environ.get('DATABASE_URL')

    conn = psycopg2.connect(url)
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS organizer (username text PRIMARY KEY, password text)")
    #replace all varchars with text, id ints with serial, lowercase all table names, add on delete cascade to some fks [[IMPORTANT]], change time to time with timezone
    cur.execute("CREATE TABLE IF NOT EXISTS tournament (tournament_id serial PRIMARY KEY, t_name text, address text, college text, city text, region text, zip text, country text, username text, FOREIGN KEY (username) REFERENCES organizer (username))")
    # [[REMOVED]] cur.execute("CREATE TABLE IF NOT EXISTS tournament_org (tournament_id serial, u_id text, PRIMARY KEY (tournament_id,u_id), FOREIGN KEY (tournament_id) REFERENCES tournament (tournament_id), FOREIGN KEY (u_id) REFERENCES organizer (username))")
    cur.execute("CREATE TABLE IF NOT EXISTS sport (sportName text PRIMARY KEY, sportType text)")
    cur.execute("INSERT INTO sport VALUES('Basketball', 'Team') ON CONFLICT DO NOTHING" )
    cur.execute("INSERT INTO sport VALUES('Football', 'Team') ON CONFLICT DO NOTHING")
    cur.execute("INSERT INTO sport VALUES('Cricket', 'Team') ON CONFLICT DO NOTHING")
    cur.execute("INSERT INTO sport VALUES('Hockey', 'Team') ON CONFLICT DO NOTHING")
    cur.execute("INSERT INTO sport VALUES('Tennis', 'Individual') ON CONFLICT DO NOTHING")
    cur.execute("INSERT INTO sport VALUES('Table Tennis', 'Individual') ON CONFLICT DO NOTHING")
    cur.execute("INSERT INTO sport VALUES('Badminton', 'Individual') ON CONFLICT DO NOTHING")
    cur.execute("CREATE TABLE IF NOT EXISTS tourn_sport (tournament_id integer, sportName text, PRIMARY KEY (tournament_id,sportName), FOREIGN KEY (tournament_id) REFERENCES tournament (tournament_id) ON DELETE CASCADE, FOREIGN KEY (sportName) REFERENCES sport (sportName))")
    cur.execute("CREATE TABLE IF NOT EXISTS player (pnum serial PRIMARY KEY, firstName text, lastName text, age integer, tournament_id integer, team_id integer)")
    cur.execute("ALTER TABLE player ADD FOREIGN KEY (tournament_id) REFERENCES tournament (tournament_id) ON DELETE CASCADE")
    cur.execute("CREATE TABLE IF NOT EXISTS team (team_id serial PRIMARY KEY, team_name text, college text, num_players integer, captain integer, sportName text, status text, contact text, FOREIGN KEY (sportName) REFERENCES sport (sportName))")
    cur.execute("ALTER TABLE team ADD FOREIGN KEY (captain) REFERENCES player (pnum) ON DELETE CASCADE")
    cur.execute("ALTER TABLE player ADD FOREIGN KEY (team_id) REFERENCES team (team_id) ON DELETE CASCADE")
    cur.execute("CREATE TABLE IF NOT EXISTS match (match_id serial PRIMARY KEY, match_date date, start_time time with time zone, tournament_id integer, sportName text, round text, matchStatus text, FOREIGN KEY (tournament_id) REFERENCES tournament (tournament_id) ON DELETE CASCADE, FOREIGN KEY (sportName) REFERENCES sport (sportName))")
    cur.execute("CREATE TABLE IF NOT EXISTS teamMatch (team_id integer, match_id integer, PRIMARY KEY (team_id,match_id), FOREIGN KEY (team_id) REFERENCES team (team_id) ON DELETE CASCADE, FOREIGN KEY (match_id) REFERENCES match (match_id) ON DELETE CASCADE)")
    cur.execute("CREATE TYPE scoreNet AS (s1t1 integer,s1t2 integer,s2t1 integer,s2t2 integer,s3t1 integer,s3t2 integer)")
    cur.execute("CREATE TYPE scoreCricket AS (t1runs integer, t1wickets integer, t2runs integer, t2wickets integer)")
    cur.execute("CREATE TYPE scoreTeams AS (t1 integer, t2 integer)")
    cur.execute("CREATE TABLE IF NOT EXISTS resultNet (winner integer, match_id integer, score scoreNet, PRIMARY KEY(winner, match_id), FOREIGN KEY (match_id) REFERENCES match (match_id) ON DELETE CASCADE)")
    cur.execute("CREATE TABLE IF NOT EXISTS resultCricket (winner integer, match_id integer, score scoreCricket, PRIMARY KEY(winner, match_id), FOREIGN KEY (match_id) REFERENCES match (match_id) ON DELETE CASCADE)")
    cur.execute("CREATE TABLE IF NOT EXISTS resultTeam (winner integer, match_id integer, score scoreTeams, PRIMARY KEY(winner, match_id), FOREIGN KEY (match_id) REFERENCES match (match_id) ON DELETE CASCADE)")
    # [[REMOVED]] cur.execute("CREATE TABLE IF NOT EXISTS Team1Score (winner integer, match_id integer, score_1 integer, PRIMARY KEY(winner, match_id,score_1), FOREIGN KEY (winner) REFERENCES Result(winner), FOREIGN KEY (match_id) REFERENCES Result (match_id))")
    # [[REMOVED]] cur.execute("CREATE TABLE IF NOT EXISTS Team2Score (winner integer, match_id integer, score_2 integer, PRIMARY KEY(winner, match_id,score_2), FOREIGN KEY (winner) REFERENCES Result(winner), FOREIGN KEY (match_id) REFERENCES Result (match_id))")

    conn.commit()
    conn.close()


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
api.add_resource(CompMatchListBySport,"/matches/completed/<int:id_>/<string:sport>")
api.add_resource(PendMatchListBySport,"/matches/pending/<int:id_>/<string:sport>")
api.add_resource(MatchListByTour, "/<int:id_>/matchList")
api.add_resource(CompMatchListByTour, "/<int:id_>/matchList/completed")
api.add_resource(PendMatchListByTour, "/<int:id_>/matchList/pending")
api.add_resource(ResultTeam,"/match/team/result/<int:mid_>")
api.add_resource(ResultNet,"/match/net/result/<int:mid_>")
api.add_resource(ResultCricket,"/match/cricket/result/<int:mid_>")
api.add_resource(TeamStatus,"/team/<string:status>")
api.add_resource(ResultListBySport, "/results/<int:id_>/<string:sport>")
api.add_resource(ResultListByTourn, "/tourn/results/<int:id_>")


if __name__ == "__main__":
    app.run(debug = True)