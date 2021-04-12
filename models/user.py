import psycopg2
import os
from flask_bcrypt import generate_password_hash,check_password_hash
from dotenv import load_dotenv
from create_tables import get_db

load_dotenv()

class UserModel:
    def __init__(self,username,password):
        self.username = username
        self.password = password

    def save_to_db(self):
        params = get_db()

        conn = psycopg2.connect(
            dbname=params[0],
            user=params[1],
            password=params[2],
            host=params[3],
            port=params[4]
            )
        cur = conn.cursor()

        cur.execute("INSERT INTO organizer VALUES (%s,%s)",(self.username,self.password))


        conn.commit()
        conn.close()


    @classmethod
    def find_by_name(cls,name):
        params = get_db()

        conn = psycopg2.connect(
            dbname=params[0],
            user=params[1],
            password=params[2],
            host=params[3],
            port=params[4]
            )
        cur = conn.cursor()

        cur.execute("SELECT * FROM organizer where username = %s",(name,))

        row = cur.fetchone()

        conn.close()

        if row:
            return cls(row[0],row[1])
        else:
            return None