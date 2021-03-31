import psycopg2
import os
from dotenv import load_dotenv

class MatchModel:
    def __init__(self,date=None,startTime=None,tournament_id=None,sportName=None):
        #self.match_id=match_id
        self.date = date
        self.startTime=startTime
        self.tournament_id=tournament_id
        self.sportName=sportName
    
    def json(self,ID):
        return {"date":str(self.date), "startTime": str(self.startTime), "tournament_id": self.tournament_id, "sportName":self.sportName,"match_id":ID}

    def save_to_db(self, t1,t2):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("INSERT INTO match VALUES (DEFAULT,%s,%s,%s,%s) RETURNING match_id", (self.date,self.startTime,self.tournament_id,self.sportName))
        match_num = cur.fetchone()[0]
        conn.commit()
        cur.execute("INSERT INTO teamMatch VALUES (%s,%s)",(t1,match_num))
        cur.execute("INSERT INTO teamMatch VALUES (%s,%s)",(t2,match_num))
        conn.commit()
        conn.close()

        return self.json(match_num)