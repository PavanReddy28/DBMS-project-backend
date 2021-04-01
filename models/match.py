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

    def findMatchesTour(tID):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()
        
        cur.execute("SELECT * from match where tournament_id = %s ORDER BY match_date,start_time",(tID,))
        rows = cur.fetchall()

        conn.close()

        if rows:
            return rows
        else:
            return None
    
    def findMatchesSport(tID,sport):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()
        
        cur.execute("SELECT * from match where tournament_id = %s and sportName = %s ORDER BY match_date,start_time",(tID,sport))
        rows = cur.fetchall()

        conn.close()

        if rows:
            return rows
        else:
            return None

    def findTeamsByMID(mID):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()
        
        cur.execute("SELECT team_id from teamMatch where match_id = %s ",(mID,))
        rows = cur.fetchall()
        #print( rows[0])

        conn.close()

        if rows:
            return rows
        else:
            return None

    def update(self,mID,dt,tm):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("UPDATE match set match_date=%s, start_time = %s where match_id = %s",(dt,tm,mID))
        conn.commit()

        cur.execute("SELECT * from match where match_id = %s",(mID,))
        row = cur.fetchone()
        
        conn.close()
        self.date = row[1]
        self.startTime = row[2]
        self.tournament_id = row[3]
        self.sportName = row[4]

        return self.json(row[0])