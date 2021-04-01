import psycopg2
import os
import json
from datetime import datetime
from flask import jsonify
from flask_restful import Resource, reqparse,inputs
from models.team import TeamModel
from models.match import MatchModel
from flask_jwt_extended import jwt_required, get_jwt_identity

class Match(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('tournament_id',
                        type=int,
                        required=True,
                        help="Tournament id cant be blank"
                        )
    parser.add_argument('team1_id',
                        type=int,
                        required=True,
                        help="Team id cant be blank"
                        )
    parser.add_argument('team2_id',
                        type=int,
                        required=True,
                        help="Team id cant be blank"
                        )
    parser.add_argument('sportName',
                        type=str,
                        required=True,
                        help="sport cant be blank"
                        )
    parser.add_argument('date',
                        type=str,#inputs.datetime_from_iso8601,
                        required=True,
                        help="date cant be blank"
                        ) 
    
    parser2 = reqparse.RequestParser()
    parser2.add_argument('tournament_id',
                        type=int,
                        required=True,
                        help="Tournament id cant be blank"
                        )
    parser2.add_argument('sportName',
                        type=str,
                        required=True,
                        help="sport cant be blank"
                        )
    parser3 = reqparse.RequestParser()
    parser3.add_argument('match_id',
                        type=int,
                        required=True,
                        help="Match id cant be blank"
                        )
    parser3.add_argument('date',
                        type=str,#inputs.datetime_from_iso8601,
                        required=True,
                        help="date cant be blank"
                        )

    @jwt_required()
    def post(self):
        data = Match.parser.parse_args()
        dt = (inputs.datetime_from_iso8601(data['date'])).date()
        tm = (inputs.datetime_from_iso8601(data['date'])).timetz()

        m = MatchModel(dt,tm,data['tournament_id'],data['sportName']).save_to_db(data['team1_id'],data['team2_id'])
        m['team1_id']=data['team1_id']
        m['team2_id']=data['team2_id']
        
        return m, 201

    @jwt_required()
    def put(self):
        data = Match.parser3.parse_args()
        print(data)
        dt = (inputs.datetime_from_iso8601(data['date'])).date()
        tm = (inputs.datetime_from_iso8601(data['date'])).timetz()

        flag = MatchModel.findTeamsByMID(data['match_id'])
        if not flag:
            return {"message": "match with id: {} does not exist".format(data['match_id'])},400
        m = MatchModel().update(data['match_id'],dt,tm)

        return m, 201


    def get(self):
        data = Match.parser2.parse_args()
        matches = MatchModel.findMatchesSport(data['tournament_id'],data['sportName'])

        sMatches = { 
            "matches": []
        }
        
        if matches:
            for m in matches:
                teams = MatchModel.findTeamsByMID(m[0])
                mat = {
                    "match_id":m[0],
                    "date":str(m[1]),
                    "startTime":str(m[2]),
                    #"sportName":m[4],
                    "team1": {"team_id":teams[0][0],"teamName":TeamModel.find_by_id(teams[0][0])[1]},
                    "team2": {"team_id":teams[1][0],"teamName":TeamModel.find_by_id(teams[1][0])[1]}
                }
                sMatches['matches'].append(mat)

        return sMatches,200


class MatchList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('tournament_id',
                        type=int,
                        required=True,
                        help="Tournament id cant be blank"
                        )

    def get(self):
        data = MatchList.parser.parse_args()
        matches = MatchModel.findMatchesTour(data['tournament_id'])

        tourMatches = { 
            "matches": []
        }
        
        if matches:
            for m in matches:
                teams = MatchModel.findTeamsByMID(m[0])
                mat = {
                    "match_id":m[0],
                    "date":str(m[1]),
                    "startTime":str(m[2]),
                    "sportName":m[4],
                    "team1": {"team_id":teams[0][0],"teamName":TeamModel.find_by_id(teams[0][0])[1]},
                    "team2": {"team_id":teams[1][0],"teamName":TeamModel.find_by_id(teams[1][0])[1]}
                }
                tourMatches['matches'].append(mat)

        return tourMatches,200




        