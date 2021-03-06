import psycopg2
import os
import json
from flask_restful import Resource, reqparse
from models.team import TeamModel
from models.player import PlayerModel
from models.tournament import TournamentModel
from flask_jwt_extended import jwt_required, get_jwt_identity

class Player(Resource):

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


class PlayerList(Resource):
    """ parser = reqparse.RequestParser()
    parser.add_argument('tournament_id',
                        type=int,
                        required=True,
                        help="Tournament id cant be blank"
                        ) """

    def get(self,id_):
        #data = PlayerList.parser.parse_args()
        participants = PlayerModel.findAll(id_,"tour")
        if not participants:
            return {"message": "tournament with id: {} does not exist".format(id_)},400

        p = { 
            "players": []
        }
        
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

class PlayerSports(Resource):
    """ parser = reqparse.RequestParser()
    parser.add_argument('tournament_id',
                        type=int,
                        required=True,
                        help="Tournament id cant be blank"
                        )
    parser.add_argument('sportName',
                        type=str,
                        required=True,
                        help="Sport cant be blank"
                        )  """          

    def get(self,id_,sport):
        #data = PlayerSports.parser.parse_args()
        t = TournamentModel.check_for_id(id_)      
        if not t:
            return {"message": "tournament with id: {} does not exist".format(id_)},400

        participants = PlayerModel.find_by_sport(id_, sport)

        p = { 
            "players": []
        }
        
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
        else:
            return {"message": "sport {} does not exist in tournament {}".format(sport,id_)},400

        return p,200