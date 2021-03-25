import psycopg2
import os
from dotenv import load_dotenv

class TournamentModel:
    def __init__(self,t_name,location,college):
        #self.tournament_id=tournament_id
        self.t_name = t_name
        self.location=location
        self.college=college

    def json(self):
        return { "t_name": self.t_name, "location": self.location, "college": self.college}

    def save_to_db(self,username):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("INSERT INTO tournament VALUES (DEFAULT,%s,%s,%s)",(self.t_name, self.location, self.college))
        conn.commit()

        cur.execute("INSERT INTO tournament_org VALUES(DEFAULT,%s)",(username,))


        conn.commit()
        conn.close()


    @classmethod
    def find_by_id(cls, username):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("SELECT * FROM tournament t where t.tournament_id in (SELECT o.tournament_id FROM tournament_org o where o.u_id = %s)",(username,))

        rows = cur.fetchall()

        conn.close()

        if rows:
            return rows
        else:
            return None
