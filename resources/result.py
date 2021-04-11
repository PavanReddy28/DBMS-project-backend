import psycopg2
import os
from flask_restful import Resource, reqparse
from models.match import MatchModel
from models.result import ResultModel
from models.sport import SportModel
from flask_jwt_extended import jwt_required, get_jwt_identity

class ResultTeam(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('winner_id',
                        type=int,
                        required=True,
                        help="winner_id cant be blank"
                        )
    """ parser.add_argument('match_id',
                        type=int,
                        required=True,
                        help="match_id cant be blank"
                        ) """
    parser.add_argument('t1Score',
                        type=int,
                        required=True,
                        help="t1Score cant be blank"
                        )
    parser.add_argument('t2Score',
                        type=int,
                        required=True,
                        help="t2Score cant be blank"
                        )
    """ parser2 = reqparse.RequestParser()                    
    parser2.add_argument('match_id',
                        type=int,
                        required=True,
                        help="match_id cant be blank"
                        ) """

    @jwt_required()
    def post(self,mid_):
        data = ResultTeam.parser.parse_args()
        res = ResultModel(data['winner_id'],mid_)
        res.insertTeam(data['t1Score'],data['t2Score'])

        m = MatchModel().find_by_id(mid_)
        teams = MatchModel.findTeamsByMID(mid_)
        m['team1ID']=teams[0][0]
        m['team2ID']=teams[1][0]
        m['winner_id']=data['winner_id']
        m['t1Score']=data['t1Score']
        m['t2Score']=data['t2Score']

        return m,201

    def get(self,mid_):
        #data = ResultTeam.parser2.parse_args()
        r = ResultModel.get_scores(mid_,'team')
        if not r:
            return {"message":"match {} has not yet concluded.".format(mid_)},400
        m = MatchModel().find_by_id(mid_)
        teams = MatchModel.findTeamsByMID(mid_)
        m['team1ID']=teams[0][0]
        m['team2ID']=teams[1][0]
        m['winner_id']=r[0]
        m['t1score']=r[1]
        m['t2score']=r[2]

        return m,200
    
    @jwt_required()
    def put(self,mid_):
        data = ResultTeam.parser.parse_args()
        res = ResultModel(data['winner_id'],mid_)
        r = ResultModel.check_for_id(mid_,'team')
        if not r:
            return {"message":"match {} has not yet concluded.".format(mid_)},400
        res.updateTeam(data['t1Score'],data['t2Score'])
        m = MatchModel().find_by_id(mid_)
        teams = MatchModel.findTeamsByMID(mid_)
        m['team1ID']=teams[0][0]
        m['team2ID']=teams[1][0]
        m['winner_id']=data['winner_id']
        m['t1Score']=data['t1Score']
        m['t2Score']=data['t2Score']

        return m,200

        
class ResultNet(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('winner_id',
                        type=int,
                        required=True,
                        help="winner_id cant be blank"
                        )
    """ parser.add_argument('match_id',
                        type=int,
                        required=True,
                        help="match_id cant be blank"
                        ) """
    parser.add_argument('set1',
                        type=dict,
                        required=True,
                        #action='append',
                        help="Set 1 cant be blank"
                        )
    parser.add_argument('set2',
                        type=dict,
                        required=True,
                        #action='append',
                        help="Set 2 cant be blank"
                        )
    parser.add_argument('set3',
                        type=dict,
                        required=False,
                        #action='append',
                        help="Set 3 cant be blank"
                        )

    """ parser2 = reqparse.RequestParser()                    
    parser2.add_argument('match_id',
                        type=int,
                        required=True,
                        help="match_id cant be blank"
                        ) """

    @jwt_required()
    def post(self,mid_):
        data = ResultNet.parser.parse_args()
        res = ResultModel(data['winner_id'],mid_)
        if data['set3']:
            res.insertNet(data['set1']['team1'],data['set1']['team2'],data['set2']['team1'],data['set2']['team2'],data['set3']['team1'],data['set3']['team2'])
        else:
            res.insertNet(data['set1']['team1'],data['set1']['team2'],data['set2']['team1'],data['set2']['team2'])

        m = MatchModel().find_by_id(mid_)
        teams = MatchModel.findTeamsByMID(mid_)
        m['team1ID']=teams[0][0]
        m['team2ID']=teams[1][0]
        m['winner_id']=data['winner_id']
        m['set1']=data['set1']
        m['set2']=data['set2']
        if data['set3']:
            m['set3']=data['set3']

        return m,201
    
    def get(self,mid_):
        #data = ResultNet.parser2.parse_args()
        r = ResultModel.get_scores(mid_,'net')
        if not r:
            return {"message":"match {} has not yet concluded.".format(mid_)},400

        m = MatchModel().find_by_id(mid_)
        teams = MatchModel.findTeamsByMID(mid_)
        m['team1ID']=teams[0][0]
        m['team2ID']=teams[1][0]
        m['winner_id']=r[0]
        m['set1']={}
        m['set2']={}
        m['set3']={}
        m['set1']['team1']=r[1]
        m['set1']['team2']=r[2]
        m['set2']['team1']=r[3]
        m['set2']['team2']=r[4]
        m['set3']['team1']=r[5]
        m['set3']['team2']=r[6]
        return m,200

    @jwt_required()
    def put(self,mid_):
        data = ResultNet.parser.parse_args()
        res = ResultModel(data['winner_id'],mid_)
        r = ResultModel.check_for_id(mid_,'net')
        if not r:
            return {"message":"match {} has not yet concluded.".format(mid_)},400

        if data['set3']:
            res.updateNet(data['set1']['team1'],data['set1']['team2'],data['set2']['team1'],data['set2']['team2'],data['set3']['team1'],data['set3']['team2'])
        else:
            res.updateNet(data['set1']['team1'],data['set1']['team2'],data['set2']['team1'],data['set2']['team2'])

        m = MatchModel().find_by_id(mid_)
        teams = MatchModel.findTeamsByMID(mid_)
        m['team1ID']=teams[0][0]
        m['team2ID']=teams[1][0]
        m['winner_id']=data['winner_id']
        m['set1']=data['set1']
        m['set2']=data['set2']
        if data['set3']:
            m['set3']=data['set3']

        return m,201
        
        
class ResultCricket(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('winner_id',
                        type=int,
                        required=True,
                        help="winner_id cant be blank"
                        )
    """ parser.add_argument('match_id',
                        type=int,
                        required=True,
                        help="match_id cant be blank"
                        ) """
    parser.add_argument('t1Innings',
                        type=dict,
                        required=True,
                        help="score cant be blank"
                        )
    parser.add_argument('t2Innings',
                        type=dict,
                        required=True,
                        help="score cant be blank"
                        )
                        
    """ parser2 = reqparse.RequestParser()                    
    parser2.add_argument('match_id',
                        type=int,
                        required=True,
                        help="match_id cant be blank"
                        ) """

    @jwt_required()
    def post(self,mid_):
        data = ResultCricket.parser.parse_args()
        res = ResultModel(data['winner_id'],mid_)
        res.insertCricket(data['t1Innings']['runs'],data['t1Innings']['wickets'],data['t2Innings']['runs'],data['t2Innings']['wickets'])

        m = MatchModel().find_by_id(mid_)
        teams = MatchModel.findTeamsByMID(mid_)
        m['team1ID']=teams[0][0]
        m['team2ID']=teams[1][0]
        m['winner_id']=data['winner_id']
        m['t1Innings']=data['t1Innings']
        m['t2Innings']=data['t2Innings']

        return m,201

    def get(self,mid_):
        #data = ResultCricket.parser2.parse_args()
        r = ResultModel.get_scores(mid_,'cricket')
        if not r:
            return {"message":"match {} has not yet concluded.".format(mid_)},400
        m = MatchModel().find_by_id(mid_)
        teams = MatchModel.findTeamsByMID(mid_)
        m['team1ID']=teams[0][0]
        m['team2ID']=teams[1][0]
        m['winner_id']=r[0]
        m['t1Innings']={}
        m['t2Innings']={}
        m['t1Innings']['runs']=r[1]
        m['t1Innings']['wickets']=r[2]
        m['t2Innings']['runs']=r[3]
        m['t2Innings']['wickets']=r[4]

        return m,200

    @jwt_required()
    def put(self,mid_):
        data = ResultCricket.parser.parse_args()
        res = ResultModel(data['winner_id'],mid_)
        r = ResultModel.check_for_id(mid_,'cricket')
        if not r:
            return {"message":"match {} has not yet concluded.".format(mid_)},400
        res.updateCricket(data['t1Innings']['runs'],data['t1Innings']['wickets'],data['t2Innings']['runs'],data['t2Innings']['wickets'])
        m = MatchModel().find_by_id(mid_)
        teams = MatchModel.findTeamsByMID(mid_)
        m['team1ID']=teams[0][0]
        m['team2ID']=teams[1][0]
        m['winner_id']=data['winner_id']
        m['t1Innings']=data['t1Innings']
        m['t2Innings']=data['t2Innings']


        return m,201


class ResultListBySport(Resource):
    def get(self,id_,sport):
        #data = Match.parser2.parse_args()
        results = ResultModel.findResultsSport(id_,sport)

        res = { 
            "results": []
        }
        
        
        if results:
            for r in results:
                #print(r)
                #teams = MatchModel.findTeamsByMID(m[0])
                if sport=="Tennis" or sport=="Table Tennis" or sport == "Badminton":
                    eachRes = {
                        "match_id":r[0],
                        "winner_id":r[1],
                        'set1':{},
                        'set2':{},
                        'set3':{}
                        
                        #"startTime":str(m[2]),
                        #"sportName":m[4],
                        #"round":m[5],
                        #"team1": {"team_id":teams[0][0],"teamName":TeamModel.find_by_id(teams[0][0])[1]},
                        #"team2": {"team_id":teams[1][0],"teamName":TeamModel.find_by_id(teams[1][0])[1]}
                    }
                    eachRes['set1']['team1']=r[2]
                    eachRes['set1']['team2']=r[3]
                    eachRes['set2']['team1']=r[4]
                    eachRes['set2']['team2']=r[5]
                    eachRes['set3']['team1']=r[6]
                    eachRes['set3']['team2']=r[7]
                    res['results'].append(eachRes)  
                elif sport=="Football" or sport=="Basketball" or sport =="Hockey":
                    eachRes = {
                        "match_id":r[0],
                        "winner_id":r[1],
                        't1score':r[2],
                        't2score':r[3]
                    }
                    res['results'].append(eachRes)  
                elif sport=="Cricket":
                    eachRes = {
                        "match_id":r[0],
                        "winner_id":r[1],
                        't1Innings':{},
                        't2Innings':{}
                    }
                    eachRes['t1Innings']['runs']=r[2]
                    eachRes['t1Innings']['wickets']=r[3]
                    eachRes['t2Innings']['runs']=r[4]
                    eachRes['t2Innings']['wickets']=r[5]
                    res['results'].append(eachRes)


        return res,200

class ResultListByTourn(Resource):
    def get(self,id_):
        #data = Match.parser2.parse_args()
        sportsL= SportModel.findSports(id_)

        sports = {}

        if sportsL:

            for i in sportsL:
                sport = i[0]
                results = ResultModel.findResultsSport(id_,sport)

                res = { 
                    "results": []
                }
                
                if results:
                    for r in results:
                        #print(r)
                        #teams = MatchModel.findTeamsByMID(m[0])
                        if sport=="Tennis" or sport=="Table Tennis" or sport == "Badminton":
                            eachRes = {
                                "match_id":r[0],
                                "winner_id":r[1],
                                'set1':{},
                                'set2':{},
                                'set3':{}
                                
                                #"startTime":str(m[2]),
                                #"sportName":m[4],
                                #"round":m[5],
                                #"team1": {"team_id":teams[0][0],"teamName":TeamModel.find_by_id(teams[0][0])[1]},
                                #"team2": {"team_id":teams[1][0],"teamName":TeamModel.find_by_id(teams[1][0])[1]}
                            }
                            eachRes['set1']['team1']=r[2]
                            eachRes['set1']['team2']=r[3]
                            eachRes['set2']['team1']=r[4]
                            eachRes['set2']['team2']=r[5]
                            eachRes['set3']['team1']=r[6]
                            eachRes['set3']['team2']=r[7]
                            res['results'].append(eachRes)  
                        elif sport=="Football" or sport=="Basketball" or sport =="Hockey":
                            eachRes = {
                                "match_id":r[0],
                                "winner_id":r[1],
                                't1score':r[2],
                                't2score':r[3]
                            }
                            res['results'].append(eachRes)  
                        elif sport=="Cricket":
                            eachRes = {
                                "match_id":r[0],
                                "winner_id":r[1],
                                't1Innings':{},
                                't2Innings':{}
                            }
                            eachRes['t1Innings']['runs']=r[2]
                            eachRes['t1Innings']['wickets']=r[3]
                            eachRes['t2Innings']['runs']=r[4]
                            eachRes['t2Innings']['wickets']=r[5]
                            res['results'].append(eachRes)
                            
                sports[sport] = res["results"]

            return sports,200
        
        else:
            return {"message":"tournament {} doesnot have sports.".format(id_)},400