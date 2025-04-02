import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("F:/project/serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancesystem-9acfd-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket':"faceattendancesystem-9acfd.appspot.com"
    
})


folderpath='F:/project/faceimg'
img_path=os.listdir(folderpath)
id_List=[]
img_List=[]
for path in img_path:
    img_List.append(cv2.imread(os.path.join(folderpath,path)))
    id_List.append(os.path.splitext(path)[0])

    filename=f'{folderpath}/{path}'
    bucket=storage.bucket()
    blob=bucket.blob(filename)
    blob.upload_from_filename(filename)

    #print(path)
    #print(os.path.splitext(path)[0])


#print(img_List)
print(id_List)

def findencode(img_List):
    encode_List=[]
    for img in img_List:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encode_List.append(encode)
    
    
       
    
    return encode_List

print('encoding started....')
encodeListImg=findencode(img_List)
encodeListImgWithId=[encodeListImg,id_List]
#print(encodeListImg)
print('encoding complete')

file=open("encodefile.p",'wb')
pickle.dump(encodeListImgWithId,file)
file.close()
print("file saved")