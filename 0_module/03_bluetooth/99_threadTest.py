import threading as th
import time 




def send():
    while(True):
        txt = input()
        #input이 자동으로 넘어가서 null 된다, bluetooth에서는 괜찮을듯 
        if(input!=None):
            print(txt)



def receive():
    while(True):
        print("hello")
        print(time.sleep(1))
    


thread1 = th.Thread(target = send)
thread2 = th.Thread(target= receive)

thread1.start()
thread2.start()