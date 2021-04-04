import psycopg2
import os
from flask_restful import Resource, reqparse
from models.team import TeamModel
from models.player import PlayerModel
from models.tournament import TournamentModel
from flask_jwt_extended import jwt_required, get_jwt_identity

class Team(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('tournament_id',
                        type=int,
                        required=True,
                        help="Tournament id cant be blank"
                        )
    parser.add_argument('team_name',
                        type=str,
                        required=True,
                        help="Team name cant be blank"
                        )
    parser.add_argument('college',
                        type=str,
                        required=True,
                        help="college cant be blank"
                        )
    parser.add_argument('num_players',
                        type=int,
                        required=True,
                        help="number of players cant be blank"
                        )
    parser.add_argument('captain',
                        type=dict,
                        required=True,
                        help="captain details cant be blank"
                        )
    parser.add_argument('sportName',
                        type=str,
                        required=True,
                        help="sport cant be blank"
                        )
    parser.add_argument('contact',
                        type=str,
                        required=True,
                        help="contact cant be blank"
                        )

    parser2 = reqparse.RequestParser()
    parser2.add_argument('tournament_id',
                        type=int,
                        required=False,
                        help="Tournament id cant be blank"
                        )
    parser2.add_argument('team_id',
                        type=int,
                        required=False,
                        help="Team id. cant be blank"
                        )
    parser2.add_argument('status_update_to',   # has to be either REJECTED or REGISTERED
                        type=str,
                        required=False,
                        help="Status cant be blank"
                        )

    def get(self):
        data = Team.parser2.parse_args()
        team = TeamModel.find_by_id(data['team_id'])
        participants = PlayerModel.findAll(data['team_id'],"team")

        if team:
            p = {
                "team_id":team[0],
                "team_name":team[1],
                "college":team[2],
                "num_players":team[3],
                "captain ID":team[4],
                "sportName":team[5],
                "contact":team[7],
                "players": []
            }
        else:
            return {"message": "team with id: {} does not exist".format(data['team_id'])},400
        
        if participants:
            for pp in participants:
                p['players'].append({
                    "pnum":pp[0],
                    "firstname":pp[1],
                    "lastname":pp[2],
                    "age":pp[3],
                    "tournament_id":pp[4],
                    "team_id":pp[5]
                })

        return p,200

    def post(self):
        data = Team.parser.parse_args()

        team = TeamModel(data['team_name'],data['college'],data['num_players'],data['sportName'],data['contact'])
        tID = team.save_to_db(data['tournament_id'])

        if not tID:
            return {"message": "team with name {} already exists in tournament {}".format(data['team_name'], data['tournament_id'])},400

        captain = PlayerModel(data['captain']['fname'], data['captain']['lname'], data['captain']['age'], data['tournament_id'],tID)
        cID = captain.save_to_db()

        team.updateCaptainID(cID,tID)

        return team.json(tID,cID), 201

    @jwt_required()
    def put(self):
        data = Team.parser2.parse_args()
        t = TeamModel.find_by_id(data['team_id'])
        if not t:
            return {"message": "team with id: {} does not exist".format(data['team_id'])},400
        
        TeamModel.updateStatus(data['team_id'],data['status_update_to'])
        return data,201

    @jwt_required()
    def delete(self):
        data = Team.parser2.parse_args()

        t = TournamentModel.check_for_id(data['tournament_id'])
        if not t:
            return {"message": "tournament with id: {} does not exist".format(data['tournament_id'])},400

        TeamModel().removeTeam(data['team_id'])

        return {"message": "team with id: {} deleted".format(data['team_id'])},201


class TeamList(Resource):

    @jwt_required()
    def get(self,id_):
        teams = TeamModel.findAll(id_)

        resTeams = { 
            "teams": []
        }
        
        if teams:
            for t in teams:
                resTeams['teams'].append({
                    "team_id":t[0],
                    "team_name":t[1],
                    "college":t[2],
                    "num_players":t[3],
                    "captain_id":t[4],
                    "sportName":t[5],
                    "status":t[6],
                    "contact":t[7]
                })

        return resTeams,200

    @jwt_required()
    def delete(self,id_):

        t = TournamentModel.check_for_id(id_)
        if not t:
            return {"message": "tournament with id: {} does not exist".format(data['tournament_id'])},400

        TeamModel().removeRejected(data['tournament_id'])

        return {"message": "rejected teams in tournament with id: {} deleted".format(data['tournament_id'])},201

    
class TeamSports(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('tournament_id',
                        type=int,
                        required=True,
                        help="Tournament id cant be blank"
                        )
    parser.add_argument('sportName',
                        type=str,
                        required=True,
                        help="Sport cant be blank"
                        )           

    def get(self):
        data = TeamSports.parser.parse_args()
        ts = TournamentModel.check_for_id(data['tournament_id'])      
        if not ts:
            return {"message": "tournament with id: {} does not exist".format(data['tournament_id'])},400

        teams = TeamModel.find_by_sport(data['tournament_id'], data['sportName'])

        resTeams = { 
            "teams": []
        }
        
        if teams:
            for t in teams:
                resTeams['teams'].append({
                    "team_id":t[0],
                    "team_name":t[1],
                    "college":t[2],
                    "num_players":t[3],
                    "captain_id":t[4],
                    "sportName":t[5],
                    "status":t[6],
                    "contact":t[7]
                })
        else:
            return {"message": "sport {} does not exist in tournament {}".format(data['sportName'],data['tournament_id'])},400

        return resTeams,200

class TeamStatus(Resource):

    @jwt_required()
    def get(self,status):

        username = get_jwt_identity()

        teams = TeamModel.find_by_status(username,status)

        data = {}

        if teams:

            for team in teams:
                print(team[0])

                team_data = {
                        "team_id": team[0],
                        "team_name": team[1],
                        "college": team[2],
                        "num_players": team[3],
                        "sport": team[4],
                        "captain_f_name": team[5],
                        "captain_l_name": team[6],
                        "contact": team[7],
                        "tournament_id": team[8]
                    }

                if team[9] in data:
                    data[team[9]].append(team_data)
                else:
                    data[team[9]] = [team_data]
        
        return data






        
