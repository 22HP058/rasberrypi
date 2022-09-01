from multiprocessing.connection import Client
import threading as th

from bluetooth import *
import pymysql
from pirc522 import RFID
import RPi.GPIO as GPIO

import time



'''----------------init----------------'''
#socket
address = ('localhost',6000)
conn = Client(address,authkey=b"pi")





#bluetooth
client_socket=BluetoothSocket( RFCOMM )
client_socket.connect(("98:D3:51:F9:28:13", 1))

warning_value = {"gas": 400, "fire" : 400,"ultraSound": 500 ,"person": 1}


#rfid
GPIO.setwarnings(False)
rfid = RFID()

stop_1_rfidId = [219,104,142,28,33] 
stop_2_rfidId = [203,172,69,28,62] 
stop_3_rfidId = [137,21,253,126,31] 

global station 
station = 1
'''----------------function----------------'''
#DB
db = pymysql.connect(host='localhost',user='root',password='pi',
db='tram',charset='utf8')
def parsingQuery(all_data):
    data = all_data.split(",")

    gas = str(data[0])
    fire = str(data[1])
    ultraSound = str(data[2])
    person = str(data[3])
    humidity =  str(data[4])
    temperature = str(data[5])

    result = {"gas":gas,"fire":fire,"ultraSound":ultraSound,"person":person,"humidity":humidity,"temperature":temperature}

    return result

def sendQuery(parsingData):
   global station 
   
   valuesList = ['NOW()','NOW()',parsingData["gas"],parsingData["fire"],parsingData["ultraSound"],parsingData["person"],parsingData["humidity"],parsingData["temperature"],str(station)]
   valuesStr = ",".join(valuesList)
   #print("Query value:",valuesStr)

   cur = db.cursor()

   q = "INSERT INTO sensor (date,time,gas,fire,ultraSound,person,humidity,temperature,station) VALUES("+valuesStr+")"
   print("Query:",q)
   cur.execute(q)

   db.commit()





'''----------------thread---------------'''
#thread1
def thread_bluetooth():
   flag = -1
   save_data = []
   while True:
      bluetooth_data = client_socket.recv(1024)
      str_data = bluetooth_data.decode("utf-8")
      list_data = list(str_data)


      for i in range(len(list_data)):
         if(list_data[i]=='s'):
            #print("start")
            flag = 1

         

         elif(list_data[i]=="f"):
            if(len(save_data)>0 and flag == 1):
               print("<------sensor data SAVE DB------>")
               bluetooth_data = "".join(save_data)
               parsing_data = parsingQuery(bluetooth_data)
               print(parsing_data)

               sendQuery(parsing_data)

               #gas, fire, ultraSound , person,trafficLight,obstacle
               sendToTram = [0,0,0,0,0,0]
               

               print("<------trigger data TO raspi(tram)------>")
               if(int(parsing_data["gas"]) > int(warning_value["gas"])):
                  sendToTram[0] = 1
               if(int(parsing_data["fire"]) < int(warning_value["fire"])):
                  sendToTram[1] = 1
               if(int(parsing_data["ultraSound"]) < int(warning_value["ultraSound"])):
                  sendToTram[2] = 1
               if(int(parsing_data["person"]) == int(warning_value["person"])):
                  sendToTram[3] = 1
               
               print(sendToTram)
               conn.send(sendToTram)

            flag = -1
            save_data = []
            parsing_data = []


         else:
            if(flag==1):
               save_data.append(list_data[i])


         
#thread2
def thread_rfid():
   while True:
      global station 

      rfid.wait_for_tag
      error,tag_type = rfid.request()
      
      #print("error:",error,end="\t")
      #print("tag_type:",tag_type)

      if not error : 
         error,uid  = rfid.anticoll()

         if(uid == stop_1_rfidId):
               station = 1
               print(station,"번 정류장")
         if(uid == stop_2_rfidId):
               station = 2
               print(station,"번 정류장")
         if(uid == stop_3_rfidId):
               station = 3
               print(station,"번 정류장")





thread1 = th.Thread(target = thread_bluetooth)
thread2 = th.Thread(target = thread_rfid)

      
thread1.start()
thread2.start()

