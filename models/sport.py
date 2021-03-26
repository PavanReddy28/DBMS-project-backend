import psycopg2
import os
from dotenv import load_dotenv

class SportModel:
    def __init__(self,sportName,sportType):
        self.sportName = sportName
        self.sportType = sportType

    def getAllSports():
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("SELECT * FROM sport")

        rows = cur.fetchall()
        
        conn.close()

        return rows 

    def save_to_db(self, id):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("INSERT INTO tourn_sport VALUES (%s,%s)",(id, self.sportName))

        conn.commit()
        conn.close()

    def findSport(self,id):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("SELECT * from tourn_sport where tournament_id = %s and sportName = %s",(id,self.sportName))
        row = cur.fetchone()
        
        conn.close()

        if row:
            return row
        else:
            return None

    def findSports(id):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("SELECT sportName from tourn_sport where tournament_id = %s",(id,))
        rows = cur.fetchall()
        
        conn.close()

        if rows:
            return rows
        else:
            return None