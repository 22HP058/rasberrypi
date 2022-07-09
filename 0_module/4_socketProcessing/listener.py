from multiprocessing.connection import Listener

address = ('localhost',6000)
listener = Listener(address,authkey=b"pi")
conn = listener.accept()


print("connection",listener.last_accepted)

while True:
    msg = conn.recv()

    print(msg)


listener.close()
