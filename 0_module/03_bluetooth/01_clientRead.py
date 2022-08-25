from bluetooth import *


 
client_socket=BluetoothSocket( RFCOMM )
#client_socket.connect(("F8:B5:4D:46:50:E5", 1))#블루투스 연결 맥주소 넣어주기
client_socket.connect(("98:D3:51:F9:28:13", 1))


flag = -1
save_data = []
while True:
   bluetooth_data = client_socket.recv(1024)
   print(bluetooth_data)



      


client_socket.close()#소켓 통신 종료