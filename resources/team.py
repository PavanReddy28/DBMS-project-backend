import psycopg2
import os
from flask_restful import Resource, reqparse
from models.team import TeamModel
from models.player import PlayerModel
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

    parser2 = reqparse.RequestParser()
    parser2.add_argument('team_id',
                        type=int,
                        required=True,
                        help="Team id. cant be blank"
                        )
    parser2.add_argument('status_update_to',
                        type=str,
                        required=True,
                        help="Status cant be blank"
                        )

    #@jwt_required()
    def post(self):
        data = Team.parser.parse_args()

        team = TeamModel(data['team_name'],data['college'],data['num_players'],data['sportName'])
        tID = team.save_to_db()

        captain = PlayerModel(data['captain']['fname'], data['captain']['lname'], data['captain']['age'], data['tournament_id'],tID)
        cID = captain.save_to_db()

        team.updateCaptainID(cID,tID)

        return team.json(tID,cID), 201

    @jwt_required()
    def put(self):
        data = Team.parser2.parse_args()
        TeamModel().updateStatus(data['team_id'],data['status_update_to'])

        return data

class TeamList(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('tournament_id',
                        type=int,
                        required=True,
                        help="Tournament id cant be blank"
                        )

    @jwt_required()
    def get(self):
        data = TeamList.parser.parse_args()
        teams = TeamModel.findAll(data["tournament_id"])

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
                    "status":t[6]
                })

        return resTeams

    

    





        
