import psycopg2
import os
from dotenv import load_dotenv
from create_tables import get_db

class TournamentModel:
    def __init__(self,t_name=None,college=None,address=None,city=None,region=None,zip_=None,country=None):
        #self.tournament_id=tournament_id
        self.t_name = t_name
        self.college=college
        self.address=address
        self.city=city
        self.region=region
        self.zip=zip_
        self.country = country

    #def json(self):
    #    return { "t_name": self.t_name, "location": self.location, "college": self.college}
    
    def json(self, id):
        return {"tournament_id":id, "t_name": self.t_name, "address": self.address, "college": self.college, "city":self.city, "region":self.region, "zip":self.zip, "country":self.country}

    def save_to_db(self,username):
        params = get_db()

        conn = psycopg2.connect(
            dbname=params[0],
            user=params[1],
            password=params[2],
            host=params[3],
            port=params[4]
            )
        cur = conn.cursor()

        cur.execute("INSERT INTO tournament (tournament_id, t_name, address, college, city, region, zip, country, username) VALUES (DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING tournament_id",(self.t_name, self.address, self.college, self.city, self.region, self.zip, self.country,username))
        id_of_new_row = cur.fetchone()[0]
        conn.commit()
        conn.close()

        return id_of_new_row


    @classmethod
    def find_by_user(cls, username):
        params = get_db()

        conn = psycopg2.connect(
            dbname=params[0],
            user=params[1],
            password=params[2],
            host=params[3],
            port=params[4]
            )
        cur = conn.cursor()

        cur.execute("SELECT * FROM tournament where username = %s",(username,))

        rows = cur.fetchall()

        conn.close()

        if rows:
            return rows
        else:
            return None
    
    def findAll():
        params = get_db()

        conn = psycopg2.connect(
            dbname=params[0],
            user=params[1],
            password=params[2],
            host=params[3],
            port=params[4]
            )
        cur = conn.cursor()

        cur.execute("SELECT * FROM tournament")

        rows = cur.fetchall()

        conn.close()

        if rows:
            return rows
        else:
            return None

    def delete_from_db(id):
        params = get_db()

        conn = psycopg2.connect(
            dbname=params[0],
            user=params[1],
            password=params[2],
            host=params[3],
            port=params[4]
            )
        cur = conn.cursor()

        cur.execute("DELETE FROM tourn_sport where tournament_id = %s",(id,))

        cur.execute("DELETE FROM tournament where tournament_id = %s",(id,))

        conn.commit()

        conn.close()

    def check_for_id(id):
        params = get_db()

        conn = psycopg2.connect(
            dbname=params[0],
            user=params[1],
            password=params[2],
            host=params[3],
            port=params[4]
            )
        cur = conn.cursor()

        cur.execute("SELECT * FROM tournament where tournament_id = %s",(id,))
        row = cur.fetchone()
        conn.close()

        if row:
            return row
        else:
            return None

    def update(self,id,t_name,address,college,city,region,zip_):
        self.t_name = t_name
        self.address = address
        self.college = college
        self.city = city
        self.region = region
        self.zip = zip_

        params = get_db()

        conn = psycopg2.connect(
            dbname=params[0],
            user=params[1],
            password=params[2],
            host=params[3],
            port=params[4]
            )
        cur = conn.cursor()

        cur.execute("UPDATE tournament SET t_name= %s, address = %s, college = %s, city = %s, region = %s, zip = %s WHERE tournament_id = %s",(t_name,address,college,city,region,zip_,id))

        conn.commit()
        conn.close()

        return self.json(id)
