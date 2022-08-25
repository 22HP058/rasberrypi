import threading as th
import time

def fun1():
    while True:
        print("fun1")
        time.sleep(1)

def fun2():
    while True:
        print("fun2")
        time.sleep(1)


thread1 = th.Thread(target = fun1)
thread2 = th.Thread(target= fun2)

thread1.start()
thread2.start()