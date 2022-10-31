import time
from datetime import datetime

#seb : rfid
from pirc522 import RFID
import RPi.GPIO as GPIO
rfid = RFID()

stop_1_rfidId = [219,104,142,28,33] 
stop_2_rfidId = [203,172,69,28,62] 
stop_3_rfidId = [137,21,253,126,31] 


#seb : firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
GPIO.setwarnings(False)

cred = credentials.Certificate("//home//pi//File//tram-e65c4-firebase-adminsdk-mguas-51f6bc11fd.json")
firebase_admin.initialize_app(cred,{'databaseURL' : "https://tram-e65c4-default-rtdb.firebaseio.com//"})
ref = db.reference("tramPlace/") #path


currentSpace = 0



while True:
    rfid.wait_for_tag
    error,tag_type = rfid.request()
    
    #print("error:",error,end="\t")
    #print("tag_type:",tag_type)

    if not error : 
        #seb : rfid button
        error,uid  = rfid.anticoll()

        #seb : time 
        currentTime = datetime.now() 
        parsingCurrentTime = currentTime.strftime('%Y-%m-%d %H:%M:%S')

        if(uid == stop_1_rfidId):
            flag = 1
            if(flag != currentSpace):
                print("<------TRAM SPACE CHANGE-> SEND FIREBASE DB------>")
                print("1번 정류장")
                currentSpace = flag
                ref.update({parsingCurrentTime:1})
                print("<------------------------------------------------>")
        if(uid == stop_2_rfidId):
            flag = 2
            if(flag != currentSpace):
                print("<------TRAM SPACE CHANGE-> SEND FIREBASE DB------>")
                print("2번 정류장")
                currentSpace = flag
                ref.update({parsingCurrentTime:2})
                print("<------------------------------------------------>")
        if(uid == stop_3_rfidId):
            flag = 3
            if(flag != currentSpace):
                print("<------TRAM SPACE CHANGE-> SEND FIREBASE DB------>")
                print("3번 정류장")
                currentSpace = flag
                ref.update({parsingCurrentTime:3})
                print("<------------------------------------------------>")


            



    