from multiprocessing.connection import Client
import time


cnt = 0

address = ('localhost',6000)
conn = Client(address,authkey=b"pi")

while(True):
    cnt += 1 
    data = "1번째: ",cnt
    conn.send(data)
    
    time.sleep(1)

conn.close()