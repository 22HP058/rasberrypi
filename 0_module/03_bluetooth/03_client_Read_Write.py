import threading as th

from bluetooth import *
 
client_socket=BluetoothSocket( RFCOMM )
client_socket.connect(("F8:B5:4D:46:50:E5", 1))
#client_socket.connect(("98:D3:51:F9:28:13", 1))

#bluetooth 값 쓰기
def send():
    while True: 
        msg = input("Send : ")
        client_socket.send(msg)    

#bluetooth 값 읽기
def receive():
    while(True):
        bluetooth_data = client_socket.recv(1024)
        print(bluetooth_data)

    
thread1 = th.Thread(target = send)
thread2 = th.Thread(target= receive)

thread1.start()
thread2.start()