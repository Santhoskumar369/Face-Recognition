import cv2
import sqlite3
import numpy as np

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam=cv2.VideoCapture(0);

def insertOrUpdate(Id,Name,Age,Case):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM Criminal WHERE ID="+str(Id)
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="UPDATE Criminal SET name='"+str(Name)+"' ,age='"+str(Age)+"' ,crime='"+str(Case)+"' WHERE ID="+str(Id)
    else:
        cmd="INSERT INTO Criminal(ID,name,age,crime) VALUES('"+str(Id)+"','"+str(Name)+"','"+str(Age)+"','"+str(Case)+"')"
        
    conn.execute(cmd)
    conn.commit()
    conn.close()
   
id=raw_input('ENTER ID')
name=raw_input('ENTER NAME')
age=raw_input('ENTER AGE')
case=raw_input('ENTER CASE')
insertOrUpdate(id,name,age,case)
sampleNum=0
while(True):
    ret,img=cam.read();
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5);
    for(x,y,w,h) in faces:
        sampleNum=sampleNum+1;
        cv2.imwrite("dataSet/User."+str(id)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.waitKey(10);
    cv2.imshow("Face",img);
    cv2.waitKey(1);
    if(sampleNum>20):
        break
cam.release()
cv2.destroyAllWindows()
