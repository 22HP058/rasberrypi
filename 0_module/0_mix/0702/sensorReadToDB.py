from bluetooth import *
import pymysql
 

#DB
db = pymysql.connect(host='localhost',user='root',password='pi',
db='tram',charset='utf8')


def sendQuery(all_data):
   data = all_data.split(",")
   fire = str(data[1])
   temperature = str(data[2])
   huminity =  str(data[3])
   air = str(data[0])

   valuesList = ['NOW()','NOW()',fire,temperature,air]
   valuesStr = ",".join(valuesList)
   print("Query value:",valuesStr)

   cur = db.cursor()

   q = "INSERT INTO sensor (date,time,fire,temperature,air) VALUES("+valuesStr+")"
   print("Query:",q)
   cur.execute(q)

   db.commit()



#BLUETOOTH 
client_socket=BluetoothSocket( RFCOMM )
#client_socket.connect(("F8:B5:4D:46:50:E5", 1))#블루투스 연결 맥주소 넣어주기
client_socket.connect(("98:D3:51:F9:28:13", 1))


flag = -1
save_data = []
while True:
   bluetooth_data = client_socket.recv(1024)
   str_data = bluetooth_data.decode("utf-8")
   list_data = list(str_data)


   for i in range(len(list_data)):
      if(list_data[i]=='s'):
         print("start")
         flag = 1

         print(save_data)
      

      elif(list_data[i]=="f"):
         print("finish")
         flag = -1
         print(save_data)
         if(len(save_data)>0):
            parsing_data = "".join(save_data)
            print(parsing_data)
            sendQuery(parsing_data)
         save_data = []


      else:
         if(flag==1):
            save_data.append(list_data[i])



      


client_socket.close()#소켓 통신 종료