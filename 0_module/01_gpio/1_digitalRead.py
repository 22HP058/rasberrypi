import RPi.GPIO as GPIO
import time 


channel = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel,GPIO.IN,pull_up_down=GPIO.PUD_UP)

while True:
    if(GPIO.input(channel)==GPIO.LOW):
        print("PUSH!")
        time.sleep(1)

GPIO.cleanup()