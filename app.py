from tensorflow.keras.models import load_model
import argparse
import cv2
import os
from flask import Flask,request,render_template
from flask_restful import Resource,Api
from start import *
import face_recognition
import numpy as np
import sqlite3
from datetime import datetime
from pyzbar import pyzbar




ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", type=str,
	default="fdm",
	help="path to face detector model directory")
ap.add_argument("-m", "--model", type=str,
	default="mask_detector.model",
	help="path to trained face mask detector model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

facedis=None
matches=None
qr_contact=None
qr_name=None
prototxtPath=None
weightsPath=None
faceNet=None
maskNet=None
path='f1'
images=[]
classNames=[]
name=None
condir={"nehul":"09999999"}
mylist=os.listdir(path)


for cls in mylist:
    curImg=cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classNames.append(os.path.splitext(cls)[0])




def findEncodings(images):
    encodeList=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown=findEncodings(images)
print(len(encodeListKnown))

def load_model1():

    global prototxtPath,weightsPath,faceNet,maskNet
    print("[INFO] loading face detector model...")
    prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
    weightsPath = os.path.sep.join([args["face"],
	"res10_300x300_ssd_iter_140000.caffemodel"])
    faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

    print("[INFO] loading face mask detector model...")
    maskNet = load_model(args["model"])

def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y , w, h = barcode.rect
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        emp_info=barcode_info.split("\n")
        qr_name=(emp_info[0])[1:]
        qr_contact=(emp_info[2])[1:]
        if barcode_info!=None:
            return "BO"
    return frame
        #print(qr_name)
    

def readqr():
    global qr_contact,qr_name
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    while ret:
        ret, frame = camera.read()
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            x, y , w, h = barcode.rect
            barcode_info = barcode.data.decode('utf-8')
            cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
            emp_info=barcode_info.split("\n")
            qr_name=(emp_info[0])[7:]
            qr_contact=(emp_info[2])[8:]
        #print(frame)
        cv2.imshow('Barcode/QR code reader', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    camera.release()
    cv2.destroyAllWindows()


app= Flask(__name__)
app.secret_key="nehul"
api= Api(app)


@app.route('/')
def index():
    return render_template('Covid.html')

ms=0
nf=0

@app.route("/predict")
def predict():
    global ms,mp,name,nf
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    c=0
    label="0"
    mp=0
    while True:
        c=c+1
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)
        for (box, pred) in zip(locs, preds):
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred
            label = "1" if mask > withoutMask else "0"
            color = (0, 255, 0) if label == "1" else (0, 0, 255)
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
            cv2.putText(frame, label, (startX, startY - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if label[0]=="0":
            mp=mp+1
        if c==18:
            ms=(label[0])
        if c>25:
            break
    cv2.destroyAllWindows()
    vs.stop()
    cap=cv2.VideoCapture(0)
    while True:
        nf=0
        success,img=cap.read()
        imgS=cv2.resize(img,(0,0),None,0.25,0.25)
        imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
        faces=face_recognition.face_locations(imgS)
        encodes=face_recognition.face_encodings(imgS,faces)

        for encodeface,faceLoc in zip(encodes,faces):
            matches=face_recognition.compare_faces(encodeListKnown,encodeface)
            facedis=face_recognition.face_distance(encodeListKnown,encodeface)
            print(facedis)
            mI=np.argmin(facedis)
            print(matches,mI,matches[mI])

            if matches[mI]:
                name=classNames[mI]
                print(name)
                nf=1
                break
        break
    return render_template('submitpage.html')

@app.route("/records")
def r1():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    cursor.execute("select * from records")
    rows=cursor.fetchall()
    connection.commit()
    connection.close()
    return render_template("reh.html",data=rows)


@app.route("/submit",methods =["GET", "POST"])
def sub():
    if request.method == "POST":
        qr_check=0
        global name
        t1=float(request.form.get("temp"))
        s1=float(request.form.get("sp"))
        ms1="Yes" if ms == "1" else "No"
        mb="No"
        if nf==1:
            name=name
        else:
            readqr()
            qr_check=1
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        print(qr_name)
        if qr_check==0:
            t="Employee"
            mname=name
            splitl1=mname.split("-")
            mname=splitl1[0]
            mcontact=condir[mname[:5].lower()]
        else:
            t="Visitor"
            mname=qr_name
            splitl2=mname.split()
            mname=splitl2[0]
            mcontact=qr_contact
        test1=(t,mname,ms1,t1,s1,mcontact)
        insert_q="INSERT INTO records(type1,name,mask,temperature,sp02,date_time,contact) VALUES(?,?,?,?,?,datetime('now', 'localtime'),?)"
        cursor.execute(insert_q,test1)
        connection.commit()
        connection.close()
        if ms=="1" and mp<2:
            mb="Yes"
        else:
            mb="No"
        dateTimeObj = datetime.now()
        d1=str(dateTimeObj.hour)+':'+str(dateTimeObj.minute)+':'+str(dateTimeObj.second)
        if t1>96 and t1<99 and s1>=95 and ms=="1" and mp<2:
            res1={'type1':t,"name":mname,'mask':mb,'temp':t1,'sp':s1,'access':"Access Granted",'time':d1}
            return render_template('result1.html',res1=res1)
        res1={'type1':t,"name":mname,'mask':mb,'temp':t1,'sp':s1,'access':"Access Denied",'time':d1}
        return render_template('result1.html',res1=res1)
        
        
    



if __name__ == "__main__":
    load_model1()
    app.run(port=5000)