import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

url = "postgresql://"+ str(os.getenv("DB_USERNAME")) + ":"+ str(os.getenv("DB_PASSWORD")) + "@localhost:5432/tournament"

conn = psycopg2.connect(url)
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS organizer (username text PRIMARY KEY, password text)")
#replace all varchars with text, id ints with serial, lowercase all table names, add on delete cascade to some fks [[IMPORTANT]], change time to time with timezone
cur.execute("CREATE TABLE IF NOT EXISTS tournament (tournament_id serial PRIMARY KEY, t_name text, address text, college text, city text, region text, zip text, country text, username text, FOREIGN KEY (username) REFERENCES organizer (username))")
# [[REMOVED]] cur.execute("CREATE TABLE IF NOT EXISTS tournament_org (tournament_id serial, u_id text, PRIMARY KEY (tournament_id,u_id), FOREIGN KEY (tournament_id) REFERENCES tournament (tournament_id), FOREIGN KEY (u_id) REFERENCES organizer (username))")
cur.execute("CREATE TABLE IF NOT EXISTS sport (sportName text PRIMARY KEY, sportType text)")
cur.execute("INSERT INTO sport VALUES('Basketball', 'Team') ON CONFLICT DO NOTHING" )
cur.execute("INSERT INTO sport VALUES('Football', 'Team') ON CONFLICT DO NOTHING")
cur.execute("INSERT INTO sport VALUES('Cricket', 'Team') ON CONFLICT DO NOTHING")
cur.execute("INSERT INTO sport VALUES('Hockey', 'Team') ON CONFLICT DO NOTHING")
cur.execute("INSERT INTO sport VALUES('Tennis', 'Individual') ON CONFLICT DO NOTHING")
cur.execute("INSERT INTO sport VALUES('Table Tennis', 'Individual') ON CONFLICT DO NOTHING")
cur.execute("INSERT INTO sport VALUES('Badminton', 'Individual') ON CONFLICT DO NOTHING")
cur.execute("CREATE TABLE IF NOT EXISTS tourn_sport (tournament_id integer, sportName text, PRIMARY KEY (tournament_id,sportName), FOREIGN KEY (tournament_id) REFERENCES tournament (tournament_id), FOREIGN KEY (sportName) REFERENCES sport (sportName))")
cur.execute("CREATE TABLE IF NOT EXISTS player (pnum serial PRIMARY KEY, firstName text, lastName text, age integer, tournament_id integer, team_id integer)")
cur.execute("ALTER TABLE player ADD FOREIGN KEY (tournament_id) REFERENCES tournament (tournament_id) ON DELETE CASCADE")
cur.execute("CREATE TABLE IF NOT EXISTS team (team_id serial PRIMARY KEY, team_name text, college text, num_players integer, captain integer, sportName text, status text, contact text, FOREIGN KEY (sportName) REFERENCES sport (sportName))")
cur.execute("ALTER TABLE team ADD FOREIGN KEY (captain) REFERENCES player (pnum) ON DELETE CASCADE")
cur.execute("ALTER TABLE player ADD FOREIGN KEY (team_id) REFERENCES team (team_id) ON DELETE CASCADE")
cur.execute("CREATE TABLE IF NOT EXISTS match (match_id serial PRIMARY KEY, match_date date, start_time time, tournament_id integer, sportName text, FOREIGN KEY (tournament_id) REFERENCES tournament (tournament_id) ON DELETE CASCADE, FOREIGN KEY (sportName) REFERENCES sport (sportName))")
cur.execute("CREATE TABLE IF NOT EXISTS teamMatch (team_id integer, match_id integer, PRIMARY KEY (team_id,match_id), FOREIGN KEY (team_id) REFERENCES team (team_id), FOREIGN KEY (match_id) REFERENCES match (match_id) ON DELETE CASCADE)")
# cur.execute("CREATE TABLE IF NOT EXISTS Result (winner integer, match_id integer, round varchar(20), PRIMARY KEY(winner, match_id), FOREIGN KEY (match_id) REFERENCES Match (match_id))")
# cur.execute("CREATE TABLE IF NOT EXISTS Team1Score (winner integer, match_id integer, score_1 integer, PRIMARY KEY(winner, match_id,score_1), FOREIGN KEY (winner) REFERENCES Result(winner), FOREIGN KEY (match_id) REFERENCES Result (match_id))")
# cur.execute("CREATE TABLE IF NOT EXISTS Team2Score (winner integer, match_id integer, score_2 integer, PRIMARY KEY(winner, match_id,score_2), FOREIGN KEY (winner) REFERENCES Result(winner), FOREIGN KEY (match_id) REFERENCES Result (match_id))")

conn.commit()
conn.close()