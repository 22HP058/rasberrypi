import pymysql

db = pymysql.connect(host='localhost',user='root',password='pi',
db='tram',charset='utf8')

cur = db.cursor()
cur.execute("SELECT * FROM sensor")
rows = cur.fetchall()

print(rows)

db.close()