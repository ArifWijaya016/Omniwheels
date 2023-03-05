import time
import cv2 
from flask import Flask, render_template, Response
import os
import RPi.GPIO as GPIO
import subprocess
import netifaces as ni
import datetime
import imutils
app = Flask(__name__)
sub = cv2.createBackgroundSubtractorMOG2()  # create background subtractor

motorA1 = 27
motorA2 = 22
motorB1 = 23
motorB2 = 24
motorC1 = 25
motorC2 = 8

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(motorA1, GPIO.OUT)
GPIO.setup(motorA2, GPIO.OUT)
GPIO.setup(motorB1, GPIO.OUT)
GPIO.setup(motorB2, GPIO.OUT)
GPIO.setup(motorC1, GPIO.OUT)
GPIO.setup(motorC2, GPIO.OUT)

ni.ifaddresses("wlan0")
ip = ni.ifaddresses("wlan0")[ni.AF_INET][0]["addr"]


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    rec=cv2.face.LBPHFaceRecognizer_create()
    rec.read("recognizer/training_data.yml")
    i = 0
    id = 0
    names = ['None', 'Ilham']
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output'+str(i)+'.avi', fourcc, 10.0, (640,480))
    # Read until video is completed
    while(cap.isOpened()):
        ret, frame = cap.read()  # import image
        frame = imutils.resize(frame, width=400)
        if not ret: #if vid finish repeat
            frame = cv2.VideoCapture(0)
            continue
        if ret:  # if there is a frame continue with code
            cv2.putText(frame, str(datetime.datetime.now()), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255),2)
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # converts image to gray
            face = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in face:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)        #cv2.imshow("countours", image)
                id,conf=rec.predict(gray[y:y+h,x:x+w])
                if(conf > 80):
                    text="Unknown"
                else :
                    text=names[id]
                #cv2.putText(frame, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0),10)
                cv2.putText(frame, text, (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0),2)
                if os.path.exists("output"+str(i)+".avi"):
                    i += 1
                out.write(frame)
                
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        #time.sleep(0.1)
        key = cv2.waitKey(20)
        if key == ord('q'):
            break
        
    out.release()
   
@app.route('/maju')
def maju():
    
    GPIO.output(motorA1, GPIO.HIGH)
    GPIO.output(motorA2, GPIO.LOW)
    GPIO.output(motorB1, GPIO.HIGH)
    GPIO.output(motorB2, GPIO.LOW)
    GPIO.output(motorC1, GPIO.LOW)
    GPIO.output(motorC2, GPIO.LOW)
    
    return render_template('index.html')

@app.route('/mundur')
def mundur():
    
    GPIO.output(motorA1, GPIO.LOW)
    GPIO.output(motorA2, GPIO.HIGH)
    GPIO.output(motorB1, GPIO.LOW)
    GPIO.output(motorB2, GPIO.HIGH)
    GPIO.output(motorC1, GPIO.LOW)
    GPIO.output(motorC2, GPIO.LOW)
    
    return render_template('index.html', ip=ip)

@app.route('/kanan')
def kanan():
    
    GPIO.output(motorA1, GPIO.HIGH)
    GPIO.output(motorA2, GPIO.LOW)
    GPIO.output(motorB1, GPIO.LOW)
    GPIO.output(motorB2, GPIO.LOW)
    GPIO.output(motorC1, GPIO.LOW)
    GPIO.output(motorC2, GPIO.LOW)
    
    return render_template('index.html')

@app.route('/kiri')
def kiri():
    
    GPIO.output(motorA1, GPIO.LOW)
    GPIO.output(motorA2, GPIO.LOW)
    GPIO.output(motorB1, GPIO.HIGH)
    GPIO.output(motorB2, GPIO.LOW)
    GPIO.output(motorC1, GPIO.LOW)
    GPIO.output(motorC2, GPIO.LOW)
    
    return render_template('index.html')

@app.route('/berhenti')
def berhenti():
    
    GPIO.output(motorA1, GPIO.LOW)
    GPIO.output(motorA2, GPIO.LOW)
    GPIO.output(motorB1, GPIO.LOW)
    GPIO.output(motorB2, GPIO.LOW)
    GPIO.output(motorC1, GPIO.LOW)
    GPIO.output(motorC2, GPIO.LOW)
    
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    #return render_template('index.html')
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


    

