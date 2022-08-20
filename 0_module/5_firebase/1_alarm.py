def listenerCallback(information):
    eventType = information.event_type
    eventData = information.data

    #제어 확인용
    '''
    print(eventType)
    print(eventData)
    ''' 
    #값 삽입만 확인 
    #규칙 지정 필요 
    if(eventType == "patch"):
        itemlist = eventData.items()
        for item in itemlist:
            print(item)

        

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("//home//pi//rasberry//0_module//5_firebase//tram-e65c4-firebase-adminsdk-mguas-7696eca7e7.json")
firebase_admin.initialize_app(cred,{'databaseURL' : "https://tram-e65c4-default-rtdb.firebaseio.com//"})

ref = db.reference()
ref.listen(listenerCallback)




