import time
from datetime import datetime

from multiprocessing.connection import Client
import threading as th

from bluetooth import *
import pymysql

from pirc522 import RFID
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

#seb : firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db



'''----------------init----------------'''
#socket
address = ('localhost',6000)
conn = Client(address,authkey=b"pi")

#bluetooth
client_socket=BluetoothSocket( RFCOMM )
client_socket.connect(("98:D3:51:F9:28:13", 1))

warning_value = {"gas": 400, "fire" : 400,"ultraSound": 500 ,"person": 1}

#firebase
cred = credentials.Certificate("//home//pi//File//tram-e65c4-firebase-adminsdk-mguas-51f6bc11fd.json")
firebase_admin.initialize_app(cred,{'databaseURL' : "https://tram-e65c4-default-rtdb.firebaseio.com//"})
ref_tramPlace = db.reference("tramPlace/") 



#rfid
GPIO.setwarnings(False)
rfid = RFID()

stop_1_rfidId = [219,104,142,28,33] 
stop_2_rfidId = [203,172,69,28,62] 
stop_3_rfidId = [137,21,253,126,31] 

global station 
station = 0



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
   
   #to mysql
   try: 
      valuesList = ['NOW()','NOW()',parsingData["gas"],parsingData["fire"],parsingData["ultraSound"],parsingData["person"],parsingData["humidity"],parsingData["temperature"],str(station)]
      valuesStr = ",".join(valuesList)
      #print("Query value:",valuesStr)

      cur = db.cursor()

      q = "INSERT INTO sensor (date,time,gas,fire,ultraSound,person,humidity,temperature,station) VALUES("+valuesStr+")"
      print("Query:",q)
      cur.execute(q)

      db.commit()

   except:
      print("!DB ERROR!")

   #toFirebase
   currentTime = datetime.now() 
   parsingCurrentTime = currentTime.strftime('%Y-%m-%d %H:%M:%S')
   humiTempGas = str(parsingData["humidity"])+","+str(parsingData["temperature"])+","+str(parsingData["gas"])
   #ref_tramInform.update({parsingCurrentTime:humiTempGas})      #seb! : 추후에 열기



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
               print("<------DB+FIREBASE : (save) SENSOR data ------>")
               bluetooth_data = "".join(save_data)
               parsing_data = parsingQuery(bluetooth_data)
               print(parsing_data)

               sendQuery(parsing_data)

               #자율 주행 판단
               #fire,ultraSound,person(sensor),trafficLight(camera),obstacle(camera)
               sendToTram = [0,0,0,0,0]
               

               print("<------TRIGGER : from arduino(SENSOR) to RASPI------>")
               if(int(parsing_data["fire"]) < int(warning_value["fire"])):
                  sendToTram[0] = 1
               if(int(parsing_data["ultraSound"]) < int(warning_value["ultraSound"])):
                  sendToTram[1] = 1
               if(int(parsing_data["person"]) == int(warning_value["person"])):
                  sendToTram[2] = 1
               
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


      if not error : 
         error,uid  = rfid.anticoll()

         #seb : time 
         currentTime = datetime.now() 
         parsingCurrentTime = currentTime.strftime('%Y-%m-%d %H:%M:%S')

         if(uid == stop_1_rfidId):
            flag = 1
            if(flag != station):
               print("<------TRAM SPACE CHANGE-> SEND FIREBASE DB------>")
               print("1번 정류장")
               station = flag
               ref_tramPlace.update({parsingCurrentTime:1})
               print("<------------------------------------------------>")
         if(uid == stop_2_rfidId):
            flag = 2
            if(flag != station):
               print("<------TRAM SPACE CHANGE-> SEND FIREBASE DB------>")
               print("2번 정류장")
               station = flag
               ref_tramPlace.update({parsingCurrentTime:2})
               print("<------------------------------------------------>")
         if(uid == stop_3_rfidId):
            flag = 3
            if(flag != station):
               print("<------TRAM SPACE CHANGE-> SEND FIREBASE DB------>")
               print("3번 정류장")
               station = flag
               ref_tramPlace.update({parsingCurrentTime:3})
               print("<------------------------------------------------>")




thread1 = th.Thread(target = thread_bluetooth)
thread2 = th.Thread(target = thread_rfid)

      
thread1.start()
thread2.start()

