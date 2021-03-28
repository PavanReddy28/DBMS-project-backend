import psycopg2
import os
import json
from flask_restful import Resource, reqparse
from models.team import TeamModel
from models.player import PlayerModel
from flask_jwt_extended import jwt_required, get_jwt_identity

class PlayerRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('tournament_id',
                        type=int,
                        required=True,
                        help="Tournament id cant be blank"
                        )
    parser.add_argument('team_id',
                        type=int,
                        required=True,
                        help="Team id cant be blank"
                        )
    parser.add_argument('players',
                        type=dict,
                        action='append',
                        required=True,
                        help="Players cant be blank"
                        )


    def post(self):
        data = Player.parser.parse_args()

        regPlayers = {
            "tournament_id":data['tournament_id'],
            "team_id":data['team_id'],
            "players":[]
        }

        for p in data['players']:
            player = PlayerModel(p['fname'],p['lname'],p['age'],data['tournament_id'],data['team_id'])
            pID = player.save_to_db()
            regPlayers['players'].append({
                "pnum":pID,
                "firstName":p['fname'],
                "lastName":p['lname'],
                "age":p['age']
            })

        cID = TeamModel().findCaptainID(data['team_id'])
        cap = PlayerModel().get_player_details(cID)
        regPlayers['captain']={
            "pnum":cID,
            "firstName":cap[0],
            "lastName":cap[1],
            "age":cap[2]
        } 

        return regPlayers, 201