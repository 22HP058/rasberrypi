
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("//home//pi//rasberry//0_module//5_firebase//tram-e65c4-firebase-adminsdk-mguas-7696eca7e7.json")
firebase_admin.initialize_app(cred,{'databaseURL' : "https://tram-e65c4-default-rtdb.firebaseio.com//"})

ref = db.reference()
ref.update({"이름":'김세빈'})



'''pip ins
doc_ref = db.collection(u'자신이 설정한 Firebase에서 컬렉션이름').document(u'문서의 이름')
doc_ref.set({
    u'CPUTemp' : 200
})
'''