import psycopg2

url = "postgresql://yash:yashenzyme@localhost:5432/yee"

# conn = psycopg2.connect(dbname='test', user='yash', password='yashenzyme', host='localhost')
conn = psycopg2.connect(url)
cur = conn.cursor()
cur.execute("""SELECT * from test""")
rows = cur.fetchall()

for row in rows:
    print("   ", row)

conn.close()