import threading as th

from bluetooth import *
 

#server ver
server_socket= BluetoothSocket(RFCOMM)

port = 1
server_socket.bind(("", port))
server_socket.listen(100)

client_socket, address = server_socket.accept()
print("Accepted connection from ", address)


def send():
    while True: 
        msg = input("Send : ")
        client_socket.send(msg)     # 전송

def receive():
    while(True):
        bluetooth_data = client_socket.recv(1024)
        print(bluetooth_data)

    
thread1 = th.Thread(target = send)
thread2 = th.Thread(target= receive)

thread1.start()
thread2.start()