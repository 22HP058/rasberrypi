from multiprocessing.connection import Listener
import threading as th


def listener1():
    address = ('localhost',6000)
    listener = Listener(address,authkey=b"pi")
    conn= listener.accept()
    print("connection1",listener.last_accepted)
    while True:
        msg = conn.recv()
        print(msg)
 



def listener2():
    address = ('localhost',6001)
    listener = Listener(address,authkey=b"pi")
    conn = listener.accept()
    print("connection2",listener.last_accepted)
    while True:
        msg = conn.recv()
        print(msg)


thread1 = th.Thread(target = listener1)
thread2 = th.Thread(target= listener2)

thread1.start()
thread2.start()



