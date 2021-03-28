import psycopg2
import os
from flask_restful import Resource, reqparse
from models.team import TeamModel
from models.player import PlayerModel
from flask_jwt_extended import jwt_required, get_jwt_identity

class TeamRegister(Resource):

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



    #@jwt_required()
    def post(self):
        data = Team.parser.parse_args()

        team = TeamModel(data['team_name'],data['college'],data['num_players'],data['sportName'])
        tID = team.save_to_db()

        captain = PlayerModel(data['captain']['fname'], data['captain']['lname'], data['captain']['age'], data['tournament_id'],tID)
        cID = captain.save_to_db()

        team.updateCaptainID(cID,tID)

        return team.json(tID,cID), 201



        
