from bluetooth import *
import pymysql
from multiprocessing.connection import Client
import time


ERROR_FIRE = 1

#DB
db = pymysql.connect(host='localhost',user='root',password='pi',
db='tram',charset='utf8')
def parsingQuery(all_data):
    data = all_data.split(",")

   #0821 DATABASE 변경
    gas = str(data[0])
    fire = str(data[1])
    ultraSound = str(data[2])
    person = str(data[3])
    humidity =  str(data[4])
    temperature = str(data[5])

    result = {"gas":gas,"fire":fire,"ultraSound":ultraSound,"person":person,"humidity":humidity,"temperature":temperature}

    return result

def sendQuery(parsingData):
   valuesList = ['NOW()','NOW()',parsingData["gas"],parsingData["fire"],parsingData["ultraSound"],parsingData["person"],parsingData["humidity"],parsingData["temperature"]]
   valuesStr = ",".join(valuesList)
   print("Query value:",valuesStr)

   cur = db.cursor()

   q = "INSERT INTO sensor (date,time,gas,fire,ultraSound,person,humidity,temperature) VALUES("+valuesStr+")"
   print("Query:",q)
   cur.execute(q)

   db.commit()



#BLUETOOTH 
client_socket=BluetoothSocket( RFCOMM )
#client_socket.connect(("F8:B5:4D:46:50:E5", 1))#블루투스 연결 맥주소 넣어주기
client_socket.connect(("98:D3:51:F9:28:13", 1))
print("socket connection:",client_socket.last_accepted)

#socket
address = ('localhost',6000)
conn = Client(address,authkey=b"pi")

print("connection",conn.last_accepted)



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
            bluetooth_data = "".join(save_data)
            print(bluetooth_data)

            parsing_data = parsingQuery(bluetooth_data)
            print(parsing_data)

            sendQuery(parsing_data)
            #이상치 넘길 시 
            if(parsing_data["fire"]>ERROR_FIRE):
                conn.send("firefire")

         save_data = []


      else:
         if(flag==1):
            save_data.append(list_data[i])



      


client_socket.close()#소켓 통신 종료