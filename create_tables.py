import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

conn = psycopg2.connect(url)
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS organizer (username text PRIMARY KEY, password text)")
#replace all varchars with text, id ints with serial, lowercase all table names
cur.execute("CREATE TABLE IF NOT EXISTS tournament (tournament_id serial PRIMARY KEY, t_name text, address text, college text, city text, region text, zip text, country text, username text, FOREIGN KEY (username) REFERENCES organizer (username))")
# [[REMOVED]] cur.execute("CREATE TABLE IF NOT EXISTS tournament_org (tournament_id serial, u_id text, PRIMARY KEY (tournament_id,u_id), FOREIGN KEY (tournament_id) REFERENCES tournament (tournament_id), FOREIGN KEY (u_id) REFERENCES organizer (username))")
cur.execute("CREATE TABLE IF NOT EXISTS sport (sportName text PRIMARY KEY, sportType text)")
cur.execute("INSERT INTO sport VALUES('Basketball', 'Team')")
cur.execute("INSERT INTO sport VALUES('Football', 'Team')")
cur.execute("INSERT INTO sport VALUES('Cricket', 'Team')")
cur.execute("INSERT INTO sport VALUES('Hockey', 'Team')")
cur.execute("INSERT INTO sport VALUES('Tennis', 'Individual')")
cur.execute("INSERT INTO sport VALUES('Table Tennis', 'Individual')")
cur.execute("INSERT INTO sport VALUES('Badminton', 'Individual')")
cur.execute("CREATE TABLE IF NOT EXISTS tourn_sport (tournament_id integer, sportName text, PRIMARY KEY (tournament_id,sportName), FOREIGN KEY (tournament_id) REFERENCES tournament (tournament_id), FOREIGN KEY (sportName) REFERENCES sport (sportName))")
# cur.execute("CREATE TABLE IF NOT EXISTS Player (pnum integer PRIMARY KEY, age integer, firstName varchar(25), lastName varchar(25), tournament_id integer, team_id integer, FOREIGN KEY (tournament_id) REFERENCES Tournament (tournament_id))")
# cur.execute("CREATE TABLE IF NOT EXISTS Team (team_id integer PRIMARY KEY, team_name varchar(50), college text, num_players integer, captain integer, sportName varchar(20), FOREIGN KEY (captain) REFERENCES Player (pnum), FOREIGN KEY (sportName) REFERENCES Sport (sportName))")
# cur.execute("ALTER TABLE Player ADD FOREIGN KEY (team_id) REFERENCES Team (team_id)")
# cur.execute("CREATE TABLE IF NOT EXISTS Match (match_id integer PRIMARY KEY, match_date date, start_time time, tournament_id integer, sportName varchar(20), FOREIGN KEY (tournament_id) REFERENCES Tournament (tournament_id), FOREIGN KEY (sportName) REFERENCES Sport (sportName))")
# cur.execute("CREATE TABLE IF NOT EXISTS TeamMatch (team_id integer, match_id integer, PRIMARY KEY (team_id,match_id), FOREIGN KEY (team_id) REFERENCES Team (team_id), FOREIGN KEY (match_id) REFERENCES Match (match_id))")
# cur.execute("CREATE TABLE IF NOT EXISTS Result (winner integer, match_id integer, round varchar(20), PRIMARY KEY(winner, match_id), FOREIGN KEY (match_id) REFERENCES Match (match_id))")
# cur.execute("CREATE TABLE IF NOT EXISTS Team1Score (winner integer, match_id integer, score_1 integer, PRIMARY KEY(winner, match_id,score_1), FOREIGN KEY (winner) REFERENCES Result(winner), FOREIGN KEY (match_id) REFERENCES Result (match_id))")
# cur.execute("CREATE TABLE IF NOT EXISTS Team2Score (winner integer, match_id integer, score_2 integer, PRIMARY KEY(winner, match_id,score_2), FOREIGN KEY (winner) REFERENCES Result(winner), FOREIGN KEY (match_id) REFERENCES Result (match_id))")

conn.commit()
conn.close()