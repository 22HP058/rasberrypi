import RPi.GPIO as GPIO
import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


GPIO.setmode(GPIO.BCM)
#speaker
GPIO.setup(24, GPIO.OUT)

#차단기
GPIO.setup(20, GPIO.OUT)
soft_pwm = GPIO.PWM(20, 50)
soft_pwm.start(10)


def listenerCallback(information):
    eventType = information.event_type
    eventPath = information.path
    eventData = information.data
    
    if(eventType == "patch"):
        itemlist = eventData.items()
        for item in itemlist:
            print(item) #2 length list [시간, 정류장]
            #1번 정류장
            if(item[1]==1):
                GPIO.output(24,True) 
                soft_pwm.ChangeDutyCycle(10) 

                time.sleep(10)
                
                GPIO.output(24,False)
                soft_pwm.ChangeDutyCycle(5)


                time.sleep(1)


                                    


        
cred = credentials.Certificate("//home//pi//File//tram-e65c4-firebase-adminsdk-mguas-51f6bc11fd.json")
firebase_admin.initialize_app(cred,{'databaseURL' : "https://tram-e65c4-default-rtdb.firebaseio.com//"})

ref = db.reference("tramPlace/")


ref.listen(listenerCallback)



