import RPi.GPIO as GPIO
import time 

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)


for i in range(10):
    print(i)
    GPIO.output(18,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(18,GPIO.LOW)
    time.sleep(2)

GPIO.cleanup()