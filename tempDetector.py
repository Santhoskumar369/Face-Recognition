
import cv2
import numpy as np
import sqlite3
import datetime
import smtplib
import config

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
rec=cv2.createLBPHFaceRecognizer();
rec.load('recognizer/trainningData.yml')
id=0
camport=0

def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(config.EMAIL_ADDRESS, "gowthumsdp@gmail.com", message)
        server.quit()
    except:
        print("Email failed to send.")


def getFromDB(Id):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM Criminal WHERE ID="+str(Id)
    cursor=conn.execute(cmd)
    record=None
    for row in cursor:
        record=row
    conn.commit()
    conn.close()
    return record

def getGps(portno):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM camloc WHERE camport="+str(portno)
    cursor=conn.execute(cmd)
    for row in cursor:
        loca=row
    conn.close()
    return loca

def criminalFound(Id,Name,Time,lat,lon):
    print Id
    subject = "CRIMINAL ALERT!!!"
    msg = "ID :"+str(Id)+"\nNAME :"+str(Name)+" has been spotted at "+str(Time)+"\nhttps://maps.google.com/?q="+str(lat)+","+str(lon)+"&hl=en&gl=in"
    send_email(subject, msg )
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM foundCriminals WHERE ID="+str(Id)
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="UPDATE foundCriminals SET name='"+str(Name)+"',time='"+str(Time)+"',lat='"+str(lat)+"',lon='"+str(lon)+"' WHERE ID="+str(Id)
    else:
        cmd="INSERT INTO foundCriminals(ID,name,time,lat,lon) VALUES('"+str(Id)+"','"+str(Name)+"','"+str(Time)+"','"+str(lat)+"','"+str(lon)+"')"        
    conn.execute(cmd)
    conn.commit()
    conn.close()

cam=cv2.VideoCapture(camport);
font=cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX_SMALL,2,1,0,4)

while(True):
    ret,img=cam.read();
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5);
    for(x,y,w,h) in faces:
        id,conf=rec.predict(gray[y:y+h,x:x+w])
        profile=getFromDB(id)
        if(conf<50):
            if(profile!=None):
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
                cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[0]),(x,y+h),font,255)
                cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[1]),(x,y+h+30),font,255)
                cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[2]),(x,y+h+60),font,255)
                cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[3]),(x,y+h+90),font,255)
                now=datetime.datetime.now();
                latlon=getGps(camport);
                criminalFound(profile[0],str(profile[1]),now,latlon[1],latlon[2])
        else:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow("Face",img);
    if(cv2.waitKey(1)==ord('q')):
       break
cam.release()
cv2.destroyAllWindows()
