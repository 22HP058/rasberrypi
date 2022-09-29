import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)
import time

#duty 비 
#https://hackerjacob.tistory.com/141

flag = 0
soft_pwm = GPIO.PWM(20, 50)
soft_pwm.start(10)
while True:

    
    if(flag == 0):
        soft_pwm.ChangeDutyCycle(10)
        flag = 1 
        print("90도")
        time.sleep(1)
    if(flag == 1):
        soft_pwm.ChangeDutyCycle(5)
        flag = 0
        print("180도")
        time.sleep(1)
    
        
    
    

soft_pwm.stop()
GPIO.cleanup()