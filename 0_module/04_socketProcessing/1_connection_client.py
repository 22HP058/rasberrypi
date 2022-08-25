from multiprocessing.connection import Client
import time


cnt = 0

address = ('localhost',6000)
conn = Client(address,authkey=b"pi")

while(True):
    cnt += 1 
    conn.send(cnt)
    
    time.sleep(1)

conn.close()