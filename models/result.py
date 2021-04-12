import psycopg2
import os
from dotenv import load_dotenv

class ResultModel:
    def __init__(self,winner=None,match_id=None,score=None):
        self.winner=winner
        self.match_id=match_id
        #self.score=score

    def insertTeam(self,t1,t2):
        url = os.environ.get['DATABASE_URL']

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("INSERT INTO resultTeam VALUES (%s,%s,ROW(%s,%s))",(self.winner,self.match_id,t1,t2))
        cur.execute("UPDATE match SET matchStatus =%s where match_id =%s",("COMPLETED",self.match_id))
        
        conn.commit()
        conn.close()

    def insertNet(self,s1t1,s1t2,s2t1,s2t2,s3t1=None,s3t2=None):
        url = os.environ.get['DATABASE_URL']

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("INSERT INTO resultNet VALUES (%s,%s,ROW(%s,%s,%s,%s,%s,%s))",(self.winner,self.match_id,s1t1,s1t2,s2t1,s2t2,s3t1,s3t2))
        cur.execute("UPDATE match SET matchStatus =%s where match_id =%s",("COMPLETED",self.match_id))
        
        conn.commit()
        conn.close()

    def insertCricket(self,t1r,t1w,t2r,t2w):
        url = os.environ.get['DATABASE_URL']

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("INSERT INTO resultCricket VALUES (%s,%s,ROW(%s,%s,%s,%s))",(self.winner,self.match_id,t1r,t1w,t2r,t2w))
        cur.execute("UPDATE match SET matchStatus =%s where match_id =%s",("COMPLETED",self.match_id))
        
        conn.commit()
        conn.close()

    def check_for_id(mID,type):
        url = os.environ.get['DATABASE_URL']

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        if type=='net':
            cur.execute("SELECT * FROM resultNet where match_id =%s",(mID,))
        elif type=='team':
            cur.execute("SELECT * FROM resultTeam where match_id =%s",(mID,))
        elif type=='cricket':
            cur.execute("SELECT * FROM resultCricket where match_id =%s",(mID,))

        row =cur.fetchone()
        conn.close()

        if row:
            return row
        else:
            return None

    def get_scores(mID,type):
        url = os.environ.get['DATABASE_URL']

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        if type=='net':
            cur.execute("SELECT winner,(score).s1t1,(score).s1t2,(score).s2t1,(score).s2t2,(score).s3t1,(score).s3t2 FROM resultNet where match_id =%s",(mID,))
        elif type=='team':
            cur.execute("SELECT winner,(score).t1,(score).t2 FROM resultTeam where match_id =%s",(mID,))
        elif type=='cricket':
            cur.execute("SELECT winner,(score).t1runs,(score).t1wickets,(score).t2runs,(score).t2wickets FROM resultCricket where match_id =%s",(mID,))

        row =cur.fetchone()
        conn.close()

        if row:
            return row
        else:
            return None

    def updateTeam(self,t1,t2):
        url = os.environ.get['DATABASE_URL']

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("UPDATE resultTeam SET winner =%s,score = ROW(%s,%s) where match_id = %s",(self.winner,t1,t2,self.match_id))
        
        conn.commit()
        conn.close()

    def updateNet(self,s1t1,s1t2,s2t1,s2t2,s3t1=None,s3t2=None):
        url = os.environ.get['DATABASE_URL']

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("UPDATE resultNet SET winner =%s,score =ROW(%s,%s,%s,%s,%s,%s) where match_id =%s",(self.winner,s1t1,s1t2,s2t1,s2t2,s3t1,s3t2,self.match_id))
        
        conn.commit()
        conn.close()

    def updateCricket(self,t1r,t1w,t2r,t2w):
        url = os.environ.get['DATABASE_URL']

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("UPDATE resultCricket SET winner =%s,score =ROW(%s,%s,%s,%s) where match_id = %s",(self.winner,t1r,t1w,t2r,t2w,self.match_id))
        
        conn.commit()
        conn.close()

    def findResultsSport(t_id,sport):
        url = os.environ.get['DATABASE_URL']

        conn = psycopg2.connect(url)
        cur = conn.cursor()
        
        if sport=="Football" or sport=="Basketball" or sport =="Hockey":
            cur.execute("SELECT r.match_id,r.winner,(score).t1,(score).t2 from resultTeam r where r.match_id in (SELECT m.match_id from match m where m.sportName=%s and m.tournament_id=%s)",(sport,t_id))
        elif sport=="Tennis" or sport=="Table Tennis" or sport == "Badminton":
            cur.execute("SELECT r.match_id,r.winner,(score).s1t1,(score).s1t2,(score).s2t1,(score).s2t2,(score).s3t1,(score).s3t2 from resultNet r where r.match_id in (SELECT m.match_id from match m where m.sportName=%s and m.tournament_id=%s)",(sport,t_id))
        elif sport=="Cricket":
            cur.execute("SELECT r.match_id,r.winner,(score).t1runs,(score).t1wickets,(score).t2runs,(score).t2wickets from resultCricket r where r.match_id in (SELECT m.match_id from match m where m.sportName=%s and m.tournament_id=%s)",(sport,t_id))
        
        rows =cur.fetchall()

        conn.close()

        if rows:
            return rows
        else :
            return None