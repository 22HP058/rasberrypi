from pirc522 import RFID

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

rfid = RFID()

while True:
    rfid.wait_for_tag
    error,tag_type = rfid.request()
    
    #print("error:",error,end="\t")
    #print("tag_type:",tag_type)

    if not error : 
        error,uid  = rfid.anticoll()

        if not error:
            print("uid:",uid)
            time.sleep(1)

    