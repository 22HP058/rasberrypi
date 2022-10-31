#seb : plus 
#multiprojecessing
from multiprocessing.connection import Listener

#firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
#for firebase format
from datetime import datetime



cred = credentials.Certificate("//home//pi//File//tram-e65c4-firebase-adminsdk-mguas-51f6bc11fd.json")
firebase_admin.initialize_app(cred,{'databaseURL' : "https://tram-e65c4-default-rtdb.firebaseio.com//"})

ref = db.reference("stationCongestion/") #path


address = ('localhost',5000)
listener = Listener(address,authkey=b"pi")
conn = listener.accept()
print("socket connection:",listener.last_accepted)



while True: 
        print("<------TRIGGER : CHANGE PEOPLE CONGESTION -> SEND FIREBASE DB------>")
        peopleCnt = conn.recv()
    
        #seb : current time
        currentTime = datetime.now() 
        parsingCurrentTime = currentTime.strftime('%Y-%m-%d %H:%M:%S')

        #seb : firebase append
        print(parsingCurrentTime,"\t",peopleCnt)
        ref.update({parsingCurrentTime:peopleCnt})




