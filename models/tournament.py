import psycopg2
import os
from dotenv import load_dotenv

class TournamentModel:
    def __init__(self,t_name=None,location=None,college=None):
        #self.tournament_id=tournament_id
        self.t_name = t_name
        self.location=location
        self.college=college

    #def json(self):
    #    return { "t_name": self.t_name, "location": self.location, "college": self.college}
    
    def json(self, id):
        return {"tournament_id":id, "t_name": self.t_name, "location": self.location, "college": self.college}

    def save_to_db(self,username):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("INSERT INTO tournament (tournament_id, t_name, location, college, username) VALUES (DEFAULT,%s,%s,%s,%s) RETURNING tournament_id",(self.t_name, self.location, self.college, username))
        id_of_new_row = cur.fetchone()[0]
        conn.commit()
        conn.close()

        return id_of_new_row


    @classmethod
    def find_by_user(cls, username):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("SELECT * FROM tournament where username = %s",(username,))

        rows = cur.fetchall()

        conn.close()

        if rows:
            return rows
        else:
            return None
    
    def findAll():
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("SELECT * FROM tournament")

        rows = cur.fetchall()

        conn.close()

        if rows:
            return rows
        else:
            return None

    def delete_from_db(id):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("DELETE FROM tournament where tournament_id = %s",(id,))

        conn.commit()

        conn.close()

    def check_for_id(id):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("SELECT * FROM tournament where tournament_id = %s",(id,))
        row = cur.fetchone()
        conn.close()

        if row:
            return row
        else:
            return None

    def update(self,id,t_name,location,college):
        self.t_name = t_name
        self.location = location
        self.college = college

        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("UPDATE tournament SET t_name= %s, location = %s, college = %s WHERE tournament_id = %s",(t_name,location,college,id))

        conn.commit()
        conn.close()

        return self.json(id)
