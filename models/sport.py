import psycopg2
import os
from dotenv import load_dotenv

class SportModel:
    def __init__(self,sportName=None,sportType=None):
        self.sportName = sportName
        self.sportType = sportType

    def getAllSports():
        url = os.environ.get['DATABASE_URL']

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("SELECT * FROM sport")

        rows = cur.fetchall()
        
        conn.close()

        return rows 

    def save_to_db(id, sportName):
        url = os.environ.get['DATABASE_URL']

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("INSERT INTO tourn_sport VALUES (%s,%s)",(id, sportName))

        conn.commit()
        conn.close()

    def findSport(self,id):
        url = os.environ.get['DATABASE_URL']

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("SELECT * from tourn_sport where tournament_id = %s and sportName = %s",(id,self.sportName))
        row = cur.fetchone()
        
        conn.close()

        if row:
            return row
        else:
            return None

    def findSports(id_):
        url = os.environ.get['DATABASE_URL']

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("SELECT sportName from tourn_sport where tournament_id = %s",(id_,))
        rows = cur.fetchall()
        
        conn.close()

        if rows:
            return rows
        else:
            return None

    def update(id, sports):
        url = os.environ.get['DATABASE_URL']

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("DELETE from tourn_sport where tournament_id = %s",(id,))
        conn.commit()
        for s in sports:
            cur.execute("INSERT INTO tourn_sport VALUES (%s,%s)",(id, s))

        conn.commit()
        conn.close()