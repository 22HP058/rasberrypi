import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)


    
GPIO.output(24,True)
time.sleep(10)
GPIO.output(24,False)

GPIO.cleanup()