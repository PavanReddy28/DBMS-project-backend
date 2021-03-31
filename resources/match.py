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

    @jwt_required()
    def post(self):
        data = Match.parser.parse_args()
        dt = (inputs.datetime_from_iso8601(data['date'])).date()
        tm = (inputs.datetime_from_iso8601(data['date'])).timetz()

        m = MatchModel(dt,tm,data['tournament_id'],data['sportName']).save_to_db(data['team1_id'],data['team2_id'])
        m['team1_id']=data['team1_id']
        m['team2_id']=data['team2_id']
        

        return m, 201