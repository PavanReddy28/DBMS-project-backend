import psycopg2
import os
from dotenv import load_dotenv

class PlayerModel:
    def __init__(self,firstName=None,lastName=None,age=None,tournament_id=None,team_id=None):
        #self.pnum=pnum
        self.firstName = firstName
        self.lastName=lastName
        self.age=age
        self.tournament_id=tournament_id
        self.team_id=team_id

    def save_to_db(self):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("INSERT INTO player (pnum, firstName, lastName, age, tournament_id, team_id) VALUES (DEFAULT,%s,%s,%s,%s,%s) RETURNING pnum", (self.firstName,self.lastName,self.age,self.tournament_id,self.team_id))
        id_of_player = cur.fetchone()[0]
        conn.commit()
        conn.close()

        return id_of_player

    def get_player_details(self,ID):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("SELECT * from player where pnum = %s", (ID,))
        row = cur.fetchone()

        conn.close()

        return row

    def findAll(id, type):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()
        
        if type == "tour":
            cur.execute("SELECT * FROM player where tournament_id = %s",(id,))
        elif type == "team":
            cur.execute("SELECT * FROM player where team_id = %s",(id,))

        rows = cur.fetchall()

        conn.close()

        if rows:
            return rows
        else:
            return None

    def find_by_sport(tID,sport):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("SELECT * FROM player p where p.tournament_id = %s AND p.team_id IN (SELECT t.team_id from team t where t.sportName = %s)",(tID,sport))

        rows = cur.fetchall()
        conn.close()

        if rows:
            return rows
        else:
            return None