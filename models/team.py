import psycopg2
import os
from dotenv import load_dotenv

class TeamModel:
    def __init__(self,team_name=None,college=None,num_players=None,sportName=None):
        #self.team_id=team_id
        self.team_name = team_name
        self.college=college
        self.num_players=num_players
        #self.captain=captain
        self.sportName=sportName

    def json(self, tID,cID):
        return {"team_id":tID, "team_name": self.team_name, "college": self.college, "num_players":self.num_players, "captain_ID":cID, "sportName":self.sportName}

    def save_to_db(self):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("INSERT INTO team (team_id, team_name, college, num_players, sportName, status) VALUES (DEFAULT,%s,%s,%s,%s,%s) RETURNING team_id",(self.team_name, self.college, self.num_players,self.sportName, "PENDING"))
        id_of_new_team = cur.fetchone()[0]

        conn.commit()
        conn.close()

        return id_of_new_team

    def updateCaptainID(self, cID,tID):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("UPDATE team SET captain = %s where team_id = %s",(cID,tID))

        conn.commit()
        conn.close()

    def findCaptainID(self,tID):
        url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

        conn = psycopg2.connect(url)
        cur = conn.cursor()

        cur.execute("SELECT captain FROM team where team_id = %s",(tID,))
        row = cur.fetchone()[0]

        conn.close()

        return row