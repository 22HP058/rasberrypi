import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
import time

#duty 비 
#https://hackerjacob.tistory.com/141

flag = 0
soft_pwm = GPIO.PWM(18, 50)
soft_pwm.start(10)
while True:

    
    if(flag == 0):
        soft_pwm.ChangeDutyCycle(10)
        flag = 1 
        print("0000000000000")
        time.sleep(1)
    if(flag == 1):
        soft_pwm.ChangeDutyCycle(5)
        flag = 0
        print("11111111111111")
        time.sleep(1)
    
        
    
    

soft_pwm.stop()
GPIO.cleanup()