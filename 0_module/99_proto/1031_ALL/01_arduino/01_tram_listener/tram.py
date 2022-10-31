from datetime import datetime
import threading as th
from multiprocessing.connection import Listener

from bluetooth import *
FORPARSING = 48
import pymysql

#seb : firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db



'''----------------init----------------''' 
#socket(from sensor)
address = ('localhost',6000)
listener = Listener(address,authkey=b"pi")
conn = listener.accept()

print("socket connection:",listener.last_accepted)

#bluetooth
client_socket=BluetoothSocket( RFCOMM )
client_socket.connect(("98:DA:60:03:D3:25", 1))

#firebase
cred = credentials.Certificate("//home//pi//File//tram-e65c4-firebase-adminsdk-mguas-51f6bc11fd.json")
firebase_admin.initialize_app(cred,{'databaseURL' : "https://tram-e65c4-default-rtdb.firebaseio.com//"})
ref_tramControl = db.reference("tramControl/") 
ref_tramEvent = db.reference("tramEvent/") 


'''----------------function----------------'''
#DB
db = pymysql.connect(host='localhost',user='root',password='pi',
db='tram',charset='utf8')
def parsingQuery(all_data):
    data = all_data.split(",")

    rcCanDrive = -int(str(data[0]))
    lineSensor_L = str(data[1])
    lineSensor_R = str(data[2])
    fireTrigger =  int(str(data[3]))-FORPARSING
    ultraSoundTrigger = int(str(data[4]))-FORPARSING
    personTrigger = int(str(data[5]))-FORPARSING
    trafficLightTrigger = int(str(data[6]))-FORPARSING
    obstacleTrigger = int(str(data[7]))-FORPARSING

    result = {"rcCanDrive":rcCanDrive,"lineSensor_L":lineSensor_L,"lineSensor_R":lineSensor_R,"gasTrigger":99,"fireTrigger":fireTrigger,"ultraSoundTrigger":ultraSoundTrigger,"personTrigger":personTrigger,"trafficLightTrigger":trafficLightTrigger,"obstacleTrigger":obstacleTrigger}

    return result

def sendQuery(parsingData):
   global station 
   #try:
   valuesList = ['NOW()','NOW()',parsingData["rcCanDrive"],parsingData["lineSensor_L"],parsingData["lineSensor_R"],parsingData["gasTrigger"],parsingData["fireTrigger"],parsingData["ultraSoundTrigger"],parsingData["personTrigger"],parsingData["trafficLightTrigger"],parsingData["obstacleTrigger"]]
   valuesList = list(map(str,valuesList))
   valuesStr = ",".join(valuesList)
   print("Query value:",valuesStr)

   cur = db.cursor()

   q = "INSERT INTO tram (date,time,rcCanDrive,lineSensor_L,lineSensor_R,gasTrigger,fireTrigger,ultraSoundTrigger,personTrigger,trafficLightTrigger,obstacleTrigger) VALUES("+valuesStr+")"
   print("Query:",q)
   cur.execute(q)
   db.commit()
    #except:
        #print("!DB ERROR!")

'''----------------thread---------------'''
#bluetooth 값 쓰기
def send():
    while True: 
        print("<------TRIGGER : from RASPI to arduino(TRAM)------>")
        msg = conn.recv()
        msg.insert(0,"s")
        msg.append("f")
        parsingMsg = ",".join(map(str, msg))
        #print(parsingMsg)
        client_socket.send(parsingMsg)



#bluetooth 값 읽기
def receive():
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
                #print("finish")
                if(len(save_data)>0 and flag == 1):
                    print("<------DB : (save) TRAM data ------>")
                    bluetooth_data = "".join(save_data)
                    parsing_data = parsingQuery(bluetooth_data)
                    print(parsing_data)
                    #to db
                    sendQuery(parsing_data)
                    #to realtime database
                    
                    currentTime = datetime.now() 
                    parsingCurrentTime = currentTime.strftime('%Y-%m-%d %H:%M:%S')

                    toFirebase = list(parsing_data.values())
                    toFirebase = list(map(str,toFirebase))
                    data_control = toFirebase[0:2]
                    data_control = ','.join(data_control)
                    data_event = toFirebase[2:-1]
                    data_event = ','.join(data_event)
                    print(data_control)
                    print(data_event)
                    #ref_tramControl.update({parsingCurrentTime:data_control}) #seb!
                    #ref_tramEvent.update({parsingCurrentTime:data_event}) #seb!
                    
                flag = -1
                save_data = []
                parsing_data = []


            else:
                if(flag==1):
                    save_data.append(list_data[i])


    
thread1 = th.Thread(target = send)
thread2 = th.Thread(target= receive)

thread1.start()
thread2.start()