from pirc522 import RFID

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

rfid = RFID()


stop_1_rfidId = [219,104,142,28,33] 
stop_2_rfidId = [203,172,69,28,62] 
stop_3_rfidId = [137,21,253,126,31] 

while True:
    rfid.wait_for_tag
    error,tag_type = rfid.request()
    
    #print("error:",error,end="\t")
    #print("tag_type:",tag_type)

    if not error : 
        error,uid  = rfid.anticoll()

        if(uid == stop_1_rfidId):
            print("1번 정류장")
        if(uid == stop_2_rfidId):
            print("2번 정류장")
        if(uid == stop_3_rfidId):
            print("3번 정류장")


    