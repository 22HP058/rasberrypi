from multiprocessing.connection import Client
import time


cnt = 0

address = ('localhost',6001)
conn = Client(address,authkey=b"pi")

while(True):
    cnt += 1 
    data = "2번째: ",cnt
    conn.send(data)
    
    time.sleep(1)

conn.close()