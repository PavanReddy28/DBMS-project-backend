import psycopg2
import os
from flask_restful import Resource, reqparse
from models.tournament import TournamentModel
from models.sport import SportModel
from flask_jwt_extended import jwt_required, get_jwt_identity

class Tournament(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('t_name',
                        type=str,
                        required=True,
                        help="Tournament name cant be blank"
                        )
    parser.add_argument('address',
                        type=str,
                        required=True,
                        help="address cant be blank"
                        )
    parser.add_argument('college',
                        type=str,
                        required=True,
                        help="college cant be blank"
                        )
    parser.add_argument('city',
                        type=str,
                        required=True,
                        help="city cant be blank"
                        )
    parser.add_argument('region',
                        type=str,
                        required=True,
                        help="region cant be blank"
                        )
    parser.add_argument('zip',
                        type=str,
                        required=True,
                        help="zip cant be blank"
                        )
    parser.add_argument('country',
                        type=str,
                        required=False,
                        help="country cant be blank"
                        )                  
    parser.add_argument('sports',
                        type=str,
                        required=False,
                        action = 'append'
                        #help="sports cant be blank"
                        )
    idParser = reqparse.RequestParser()
    idParser.add_argument('tournament_id',
                        type=int,
                        required=True,
                        help="Tournament id cant be blank"
                        )

    @jwt_required()
    def get(self):
        user = get_jwt_identity()
        tournaments = TournamentModel.find_by_user(user)

        userTournaments = { 
            "tournaments": []
        }
        
        if tournaments:
            for t in tournaments:
                data = {
                    "tournament_id":t[0],
                    "t_name":t[1],
                    "address":t[2],
                    "college":t[3],
                    "city": t[4],
                    "region": t[5],
                    "zip": t[6],
                    "country": t[7],
                    "sports": [sport[0] for sport in SportModel.findSports(t[0])]

                }
                userTournaments['tournaments'].append(data)

        
        return userTournaments
        
    @jwt_required()
    def post(self):
        user = get_jwt_identity()
        
        data = Tournament.parser.parse_args()

        tournament = TournamentModel(data['t_name'],data['college'],data['address'],data['city'],data['region'],data['zip'],data['country'])
        id_of_new_row = tournament.save_to_db(user)


        for s in data['sports']:
            SportModel.save_to_db(id_of_new_row, s)
        
        ret = tournament.json(id_of_new_row)
        ret['sports']= data['sports']
        return ret, 201

    @jwt_required()
    def delete(self):
        data = Tournament.idParser.parse_args()

        t = TournamentModel.check_for_id(data['tournament_id'])

        if not t:
            return {"message": "tournament with id: {} does not exist".format(data['tournament_id'])},400

        TournamentModel.delete_from_db(data['tournament_id'])

        return {
            "message":"tournament with {} deleted".format(data["tournament_id"])
        }

    @jwt_required()
    def put(self):
        dataID = Tournament.idParser.parse_args()
        data = Tournament.parser.parse_args()

        t = TournamentModel.check_for_id(dataID['tournament_id'])

        if not t:
            return {"message": "tournament with id: {} does not exist".format(data['tournament_id'])},400

        t2 = TournamentModel()
        t3= t2.update(dataID['tournament_id'], data['t_name'],data['address'],data['college'],data['city'],data['region'],data['zip'])
        SportModel.update(dataID['tournament_id'],data['sports'])

        t3['sports']= data['sports']

        return t3,201


class TournamentList(Resource):

    def get(self):
        tournaments = TournamentModel.findAll()

        userTournaments = { 
            "tournaments": []
        }
        
        if tournaments:
            for t in tournaments:
                userTournaments['tournaments'].append({
                    "tournament_id":t[0],
                    "t_name":t[1],
                    "address":t[2],
                    "college":t[3],
                    "city":t[4],
                    "region":t[5],
                    "zip":t[6],
                    "country":t[7],
                    "sports": [sport[0] for sport in SportModel.findSports(t[0])]
                })

        
        return userTournaments
        