import pymysql
import time 

#data ERROR(NOW()로 변경)
'''
t = time.localtime(time.time())
date = time.strftime('%Y-%m-%d',t)
times = time.strftime('%H:%M:%S',t)

'''

fire = str(30)
temperature = str(20)
air = str(100)
valuesList = ['NOW()','NOW()',fire,temperature,air]
valuesStr = ",".join(valuesList)
print(valuesStr)

#query for db
db = pymysql.connect(host='localhost',user='root',password='pi',
db='tram',charset='utf8')

cur = db.cursor()

q = "INSERT INTO sensor (date,time,fire,temperature,air) VALUES("+valuesStr+")"
print(q)
cur.execute(q)

db.commit()

db.close()