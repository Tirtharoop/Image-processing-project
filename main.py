import cv2
import cvzone
import numpy as np
import os
import csv
import face_recognition
import pickle
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("F:/project/serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancesystem-9acfd-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket':"faceattendancesystem-9acfd.appspot.com"
    
})

bucket=storage.bucket()
matchIndex=0


cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

imgbackground=cv2.imread('F:/project/background.png')
#dim=(1000,500)
#imgbackground=cv2.resize(imgbackground,dim)

#importing the images into list
folderpath_face='F:/project/faceimg'
img_path_face=os.listdir(folderpath_face)
id_List_face=[]
#img_List_face=[]
for path in img_path_face:
    #img_List_face.append(cv2.imread(os.path.join(folderpath_face,path)))
    id_List_face.append(os.path.splitext(path)[0])



foldermodepath='F:/project/images'
img_path_list=os.listdir(foldermodepath)
img_list=[]
for path in img_path_list:
    img_list.append(cv2.imread(os.path.join(foldermodepath,path)))

print(len(img_list))

now = datetime.now()
current_date=now.strftime("%Y-%m-%d")
f=open(current_date+ '.csv','w+',newline='')
lnwriter = csv.writer(f)

#load the encoding file
print('loading the file......')
file=open('encodefile.p','rb')
encodeListImgWithId=pickle.load(file)
file.close()
encodeListImg,id_List=encodeListImgWithId
print(id_List)
print('encode file loaded')


modeType=0
counter=0
id=-1
imgstudent=[]

while True:
    sucess,img=cap.read()
    
    imgs=cv2.resize(img,(0,0),None,0.25,0.25)
    imgs=cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB)

    faceCurFrame=face_recognition.face_locations(imgs)
    encodeCurFrame=face_recognition.face_encodings(imgs,faceCurFrame)

    imgbackground[162:162+480,55:55+640]=img
    imgbackground[44:44+633,808:808+414]=img_list[modeType]

    if faceCurFrame:
         

        for encodeFace,Faceloc in zip(encodeCurFrame,faceCurFrame):
            matches=face_recognition.compare_faces(encodeListImg,encodeFace)
            faceDis=face_recognition.face_distance(encodeListImg,encodeFace)
            #print('matches',matches)
            #print('faceDis',faceDis)

            matchIndex=np.argmin(faceDis)
            #print("index",matchIdex)

            if matches[matchIndex]:
                #print('face detected')
                #print(id_List[matchIndex])
                id=id_List[matchIndex]
                temp=str(id)
                if counter ==0:
                   #cvzone.putTextRect(imgbackground,"Loading",(275,400))
                   #cv2.imshow("back",imgbackground)
                   #cv2.waitKey(1)

                   counter=1
                   modeType=1

            
        

        folderpath_face='F:/project/faceimg'
        img_path_face=os.listdir(folderpath_face)
        #id_List_face=[]
        img_List_face=[]
        for path in img_path_face:
            img_List_face.append(cv2.imread(os.path.join(folderpath_face,path)))
            #id_List_face.append(os.path.splitext(path)[0])
        
        
        
        if counter!=0:

            if counter ==1:
                #get the data
                studentInfo=db.reference(f'students/{id}').get()
                print(studentInfo)
                #get the image from storage
                #blob=bucket.get_blob(f'F:/project/faceimg/{id}.png')
                #arr=np.frombuffer(blob.download_as_string(),np.uint8)
                #imgstudent=cv2.imdecode(arr,cv2.COLOR_BGRA2BGR)
                #imgstudent=cv2.imread(f'F:/project/faceimg/{id}.png',1)
                #imgstudent=str(imgstudent)
                #cv2.imshow('img',imgstudent)
                
                
                #update data of attendance
                dateTimeObject=datetime.strptime(studentInfo['last_attendance'], "%Y-%m-%d %H:%M:%S")
                SecElapsed=(datetime.now()-dateTimeObject).total_seconds()
                print(SecElapsed)
                if SecElapsed>30:
                    ref=db.reference(f'students/{id}')
                    studentInfo['total_attendance']+=1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    current_time=now.strftime("%H:%M:%S")
                    lnwriter.writerow([str(studentInfo['name']),current_time])
                else:
                    modeType=3
                    counter=0
                    imgbackground[44:44+633,808:808+414]=img_list[modeType]
            
            if modeType!=3:
                if 10<counter<40:
                    modeType=2

                imgbackground[44:44+633,808:808+414]=img_list[modeType]    





                if counter<=10:
                    cv2.putText(imgbackground,str(studentInfo['total_attendance']),(861,125),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                    cv2.putText(imgbackground,str(studentInfo['major']),(1006,550),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                    cv2.putText(imgbackground,str(id),(1006,493),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                    cv2.putText(imgbackground,str(studentInfo['standing']),(910,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                    cv2.putText(imgbackground,str(studentInfo['year']),(1025,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                    cv2.putText(imgbackground,str(studentInfo['starting_year']),(1125,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)

                    (w,h),_= cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
                    offset=(414-w)//2

                    cv2.putText(imgbackground,str(studentInfo['name']),(808+offset,445),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)
                    

                    for i in range(len(id_List_face)):
                        if id_List_face[i] ==temp:
                            imgbackground[175:175+216,909:909+220]=img_List_face[i]
            

                counter+=1

                if counter>=20:
                    counter=0
                    modeType=0
                    studentInfo=[]
                    img_List_face=[]
                    imgbackground[44:44+633,808:808+414]=img_list[modeType]
    else:
        modeType=0
        counter=0

    
     


    


    #cv2.imshow("face",img)
    cv2.imshow("back",imgbackground)
    k= cv2.waitKey(1)
    if k%256 == 27:
        break





