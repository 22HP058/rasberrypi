import threading as th
from multiprocessing.connection import Listener


from bluetooth import *
 

#bluetooth
#server ver
server_socket= BluetoothSocket(RFCOMM)

port = 1
server_socket.bind(("", port))
server_socket.listen(100)

client_socket, address = server_socket.accept()
print("bluetooth connection: ", address)


#socket(from sensor)
address = ('localhost',6000)
listener = Listener(address,authkey=b"pi")
conn = listener.accept()

print("socket connection:",listener.last_accepted)


#bluetooth 값 쓰기
def send():
    while True: 
        msg = conn.recv()
        print(msg)
        client_socket.send(str(msg))     

#bluetooth 값 읽기
#+tram database 삽입 
def receive():
    while(True):
        bluetooth_data = client_socket.recv(1024)
        print(bluetooth_data)

    
thread1 = th.Thread(target = send)
thread2 = th.Thread(target= receive)

thread1.start()
thread2.start()