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

    def save_to_db(self,user):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("INSERT INTO tournament VALUES (DEFAULT,%s,%s,%s)",(self.t_name, self.location, self.college))
        conn.commit()

        cur.execute("INSERT INTO tournament_org VALUES(DEFAULT,%s)",(user,))


        conn.commit()
        conn.close()


    @classmethod
    def find_by_id(cls, id):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("SELECT * FROM tournament where tournament_id = %s",(id,))

        row = cur.fetchone()

        conn.close()

        if row:
            return cls(*row)
        else:
            return None
