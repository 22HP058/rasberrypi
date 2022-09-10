import threading as th
from multiprocessing.connection import Listener


from bluetooth import *
import pymysql



'''----------------init----------------''' 
#socket(from sensor)
address = ('localhost',6000)
listener = Listener(address,authkey=b"pi")
conn = listener.accept()

print("socket connection:",listener.last_accepted)



#bluetooth
client_socket=BluetoothSocket( RFCOMM )
client_socket.connect(("98:DA:60:03:D3:25", 1))


'''----------------function----------------'''
#DB
db = pymysql.connect(host='localhost',user='root',password='pi',
db='tram',charset='utf8')
def parsingQuery(all_data):
    data = all_data.split(",")

    rcCanDrive = str(data[0])
    lineSensor_L = str(data[1])
    lineSensor_R = str(data[2])
    gasTrigger = str(data[3])
    fireTrigger =  str(data[4])
    ultraSoundTrigger = str(data[5])
    personTrigger = str(data[6])
    trafficLightTrigger = str(data[7])
    obstacleTrigger = str(data[8])

    result = {"rcCanDrive":rcCanDrive,"lineSensor_L":lineSensor_L,"lineSensor_R":lineSensor_R,"gasTrigger":gasTrigger,"fireTrigger":fireTrigger,"ultraSoundTrigger":ultraSoundTrigger,"personTrigger":personTrigger,"trafficLightTrigger":trafficLightTrigger,"obstacleTrigger":obstacleTrigger}

    return result

def sendQuery(parsingData):
   global station 
   
   valuesList = ['NOW()','NOW()',parsingData["rcCanDrive"],parsingData["lineSensor_L"],parsingData["lineSensor_R"],parsingData["gasTrigger"],parsingData["fireTrigger"],parsingData["ultraSoundTrigger"],parsingData["personTrigger"],parsingData["trafficLightTrigger"],parsingData["obstacleTrigger"]]
   valuesStr = ",".join(valuesList)
   #print("Query value:",valuesStr)

   cur = db.cursor()

   q = "INSERT INTO tram (date,time,rcCanDrive,lineSensor_L,lineSensor_R,gasTrigger,fireTrigger,ultraSoundTrigger,personTrigger,trafficLightTrigger,obstacleTrigger) VALUES("+valuesStr+")"
   print("Query:",q)
   cur.execute(q)

   db.commit()

'''----------------thread---------------'''
#bluetooth 값 쓰기
def send():
    while True: 
        print("<------trigger data FROM raspi(sensor) TO tram------>")
        msg = conn.recv()
        msg.insert(0,"s")
        msg.append("f")
        parsingMsg = ",".join(map(str, msg))
        print(parsingMsg)
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
                    print("<------tram data SAVE DB------>")
                    bluetooth_data = "".join(save_data)
                    parsing_data = parsingQuery(bluetooth_data)
                    print(parsing_data)

                    sendQuery(parsing_data)

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