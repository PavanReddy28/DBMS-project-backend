import psycopg2
import os
from flask_bcrypt import generate_password_hash,check_password_hash
from dotenv import load_dotenv

load_dotenv()

class UserModel:
    def __init__(self,username,password):
        self.username = username
        self.password = password

    def save_to_db(self):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("INSERT INTO organizer VALUES (%s,%s)",(self.username,self.password))


        conn.commit()
        conn.close()


    @classmethod
    def find_by_name(cls,name):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("SELECT * FROM organizer where username = %s",(name,))

        row = cur.fetchone()

        conn.close()

        if row:
            return cls(row[0],row[1])
        else:
            return None