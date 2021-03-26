import psycopg2
import os
from flask_restful import Resource, reqparse
from models.sport import SportModel
from flask_jwt_extended import jwt_required, get_jwt_identity

class Sport(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('tournament_id',
                        type=str,
                        required=True,
                        help="Tournament id cant be blank"
                        )
    parser.add_argument('sportName',
                        type=str,
                        required=True,
                        help="sport cant be blank"
                        )
    parser.add_argument('sportType',
                        type=str,
                        required=True,
                        help="sport type cant be blank"
                        )


    @jwt_required()
    def get(self):         # gets all sports from the Sport table for the organizer to choose from
        sportsAvailable = SportModel.getAllSports()

        getSports = { 
            "sports": []
        }
        
        if sportsAvailable:
            for s in sportsAvailable:
                getSports['sports'].append({
                    "sportName":s[0],
                    "sportType":s[1],
                })

        return getSports

    @jwt_required()
    def post(self):         # posts the chosen sports for the chosen tournament into the tourn_sports table
        data = Sport.parser.parse_args()

        sport = SportModel(data['sportName'],data['sportType'])
        s = sport.findSport(data['tournament_id'])
        if not s:
            sport.save_to_db(data['tournament_id'])

            return {        
               "message":"sport {} added to tournament {}".format(data["sportName"],data["tournament_id"])
            }
        return {        
               "message":"sport {} already exists in tournament {}".format(data["sportName"],data["tournament_id"])
        }

class SportList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('tournament_id',
                        type=str,
                        required=True,
                        help="Tournament id cant be blank"
                        )

    def get(self):           # gets all sports for a given tournament
        data = SportList.parser.parse_args()
        sports = SportModel.findSports(data["tournament_id"])

        tSports = { 
            "sports": []
        }
        
        if sports:
            for s in sports:
                tSports['sports'].append({
                    "sportName":s[0]
                })

        
        return tSports