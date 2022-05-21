import os
import json

from flask import Flask, jsonify, request, render_template, Response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import requests
import cv2
import eyeblink
import blinkduration
from firebase import Firebase 
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials
from datetime import datetime
import urllib.request 
from urllib.parse import unquote
from urllib.parse import urlparse


config = {
  "apiKey": "AIzaSyCnoKv8shJVI32bQ-NT9fPKWppeo8yFn7Q",
  "authDomain": "eye-examination-database.firebaseapp.com",
  "databaseURL": "https://eye-examination-database-default-rtdb.firebaseio.com",
  "projectId": "eye-examination-database",
  "storageBucket": "eye-examination-database.appspot.com",
}


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "eye-examination-database-firebase-adminsdk-uw2sl-f0e23442f4.json"
cred = credentials.Certificate("eye-examination-database-firebase-adminsdk-uw2sl-f0e23442f4.json")
firebase_admin.initialize_app(cred)
firebase = Firebase(config)
storage = firebase.storage()


app = Flask(__name__)
app.config.from_object(__name__)
secret_key = '569b9653d72565a63435e873bbab94ed'
#569b9653d72565a63435e873bbab94ed
app.config['SECRET_KEY'] = secret_key

APP_FOLDER = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(APP_FOLDER,'download')

app.config['APP_FOLDER'] = APP_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

valueList={}
db = firestore.Client()
# @app.route('/checkKey')
# def checkPath():
#     key = request.headers.get('key')
#     print(key)
#     return str(key)


@app.route('/')
def hello():
    return render_template('upload.html')

@app.route('/getFile-<files>')
def getFile(files):
    #if request.headers.get('key') == secret_key:
    return str(files) 


@app.route('/getPath')
def getPath():
    return str(APP_FOLDER + ' ' + DOWNLOAD_FOLDER)

@app.route('/downloadVideo')
def downloadVideo():
    storage.child("video_mockup/test.mp4").download(os.path.join(DOWNLOAD_FOLDER,'mockup.mp4'))
    return 'video uploaded successfully'
    # else:
    #     return 'failed'

@app.route('/checkBody', methods=['POST'])
def checkBody():
    if request.method == 'POST':
        body = request.json
        key = body['key']
        return key
         

@app.route('/checkHeader')
def checkHeader():
    header = request.headers.get('key')
    print(header)
    return str(header)


@app.route('/downloadURL', methods= ['post'])
def downloadURL():
    if request.method == 'POST':
        url_link = request.args['url']
    #https%3A%2F%2Ffirebasestorage.googleapis.com%2Fv0%2Fb%2Feye-examination-database.appspot.com%2Fo%2Ffiles%252FREC2570387848447835707.mp4%3Falt%3Dmedia%26token%3D93d5ef70-0b18-41db-b915-a91539a3a453
        print(url_link)
        uncodeURL = unquote(url_link)
        parseURL = urlparse(uncodeURL)
        videoName = os.path.basename(parseURL.path)
        urllib.request.urlretrieve(url_link,os.path.join(DOWNLOAD_FOLDER,videoName))
        return 'video downloaded successfully' 



app.route('/eyetesthalf')
def eyeTestHalf():
    videoname = request.args['video']
    #video = '5.mp4'
    video = videoname 
    total , timer , realtimer , countdown = eyeblink.eyeblink_halfframe(video)
    status = ''
    if total == 0:
        status = 'Not Eye Detected'
    else:
        if timer == 30 and countdown > 0:
            status = 'too long video'
        elif timer == 30 and countdown == 0:
            status = 'OK video'
        elif timer < 30 and countdown == 0:
            status = 'too short video'

    print('interval time : ' + str(realtimer))
    print('total blink : ' + str(total) )
    print('status : ' + str(status))
    return('eyetest testing success')

@app.route('/eyetest')
def eyeTest():
    videoname = request.args['video']
    #video = '5.mp4'
    video = videoname 
    total , timer , realtimer , countdown = eyeblink.eyeblink(video)
    status = ''
    if total == 0:
        status = 'Not Eye Detected'
    else:
        if timer == 30 and countdown > 0:
            status = 'too long video'
        elif timer == 30 and countdown == 0:
            status = 'OK video'
        elif timer < 30 and countdown == 0:
            status = 'too short video'
    
    print('interval time : ' + str(realtimer))
    print('total blink : ' + str(total) )
    print('status : ' + str(status))
    return('eyetest testing success')

@app.route('/eyetest2')
def eyeTestTest():
    videoname = request.args['video']
    #video = '5.mp4'
    video = videoname 
    total , timer , realtimer , countdown = eyeblink.eyeblink_halfframe(video)
    status = ''
    if total == 0:
        status = 'Not Eye Detected'
    else:
        if timer == 30 and countdown > 0:
            status = 'too long video'
        elif timer == 30 and countdown == 0:
            status = 'OK video'
        elif timer < 30 and countdown == 0:
            status = 'too short video'
            
    print('interval time : ' + str(realtimer))
    print('total blink : ' + str(total) )
    print('status : ' + str(status))
    return('eyetest testing success')

@app.route('/blinktest')
def blinkTest():
    #video = '5.mp4'
    videoname = request.args['video']
    #video = '5.mp4'
    video = videoname 
    total , duration , timer = blinkduration.blinkduration(video)
    status = ''
    if total == 0:
        status = 'Not Eye Detected'
    else:
        if duration > 30:
            status = 'too long video'
        elif duration == 30:
            status = 'OK video'
        else: 
            status = 'too short video'

    print('interval time : ' + str(timer) )
    print('total blink : ' + str(total) )
    print('status : ' + str(status))
    return('blinktest testing success')


@app.route('/eyeblink', methods=['POST'])
def getEyeblink():
     if request.method == 'POST':
        body = request.json
        key = body['key']
        url_link = request.args['url']
        print(url_link)
        uncodeURL = unquote(url_link)
        parseURL = urlparse(uncodeURL)
        videoName = os.path.basename(parseURL.path)
        urllib.request.urlretrieve(url_link,os.path.join(DOWNLOAD_FOLDER,videoName))
        json_dict = {}
        total , timer , realtimer , countdown  = eyeblink.eyeblink(videoName)
        status = ''
        if total == 0:
            status = 'Not Eye Detected'
        else:
            if timer == 30 and countdown > 0:
                status = 'too long video'
            elif timer == 30 and countdown == 0:
                status = 'OK video'
            elif timer < 30 and countdown == 0:
                status = 'too short video'
        print('interval time : ' + str(realtimer) )
        print('total blink : ' + str(total) )
        print('status : ' + str(status))
        firebase = Firebase(config)
        valueList['BlinkFrequency'] = total 
        data = {
            u'name':videoName, u'eyeblink':total, u'status':status,
        }
        try:
            db.collection(u'dryeye').document(key).update(data)
        except:
            db.collection(u'dryeye').document(key).set(data)
        return 'BlinkFrequency Success'

        
@app.route('/blinkduration', methods=['POST'])
def getBlinkduration():
     if request.method == 'POST':
        body = request.json
        key = body['key']
        url_link = request.args['url']
        print(url_link)
        uncodeURL = unquote(url_link)
        parseURL = urlparse(uncodeURL)
        videoName = os.path.basename(parseURL.path)
        urllib.request.urlretrieve(url_link,os.path.join(DOWNLOAD_FOLDER,videoName))
        json_dict = {}
        total , duration , timer = blinkduration.blinkduration(videoName)
        status = ''
        if total == 0:
            status = 'Not Eye Detected'
        else:
            if duration > 30:
                status = 'too long video'
            elif duration == 30:
                status = 'OK video'
            else: 
                status = 'too short video'

        print('interval time : ' + str(timer) )
        print('total blink : ' + str(total) )
        print('status : ' + str(status))
        firebase = Firebase(config)
        data = {
            u'name':videoName, u'duration':timer, u'status':status,
        }
        valueList['IntervalTime'] = timer 
        try:
            db.collection(u'dryeye').document(key).update(data)
        except:
            db.collection(u'dryeye').document(key).set(data)
        return 'IntervalTime Success'
 


async def blinkProcess(videoName):
    total , timer , realtimer , countdown = eyeblink.eyeblink(videoName)
    return total , timer , realtimer , countdown

async def timeProcess(videoName):
    total , duration , timer = blinkduration.blinkduration(videoName)
    return total , duration , timer

@app.route('/eyeblink-async', methods=['POST'])
async def getEyeblinkAsync():
     if request.method == 'POST':
        body = request.json
        key = body['key']
        url_link = request.args['url']
        print(url_link)
        uncodeURL = unquote(url_link)
        parseURL = urlparse(uncodeURL)
        videoName = os.path.basename(parseURL.path)
        urllib.request.urlretrieve(url_link,os.path.join(DOWNLOAD_FOLDER,videoName))
        json_dict = {}
        total , timer , realtimer , countdown  = await blinkProcess(videoName)
        status = ''
        if total == 0:
            status = 'Not Eye Detected'
        else:
            if timer == 30 and countdown > 0:
                status = 'too long video'
            elif timer == 30 and countdown == 0:
                status = 'OK video'
            elif timer < 30 and countdown == 0:
                status = 'too short video'
        print('interval time : ' + str(realtimer) )
        print('total blink : ' + str(total) )
        print('status : ' + str(status))
        firebase = Firebase(config)
        valueList['BlinkFrequency'] = total 
        data = {
            u'name':videoName, u'eyeblink':total, u'status':status,
        }
        try:
            db.collection(u'dryeye').document(key).update(data)
        except:
            db.collection(u'dryeye').document(key).set(data)
        return 'BlinkFrequency Success'

        
@app.route('/blinkduration-async', methods=['POST'])
async def getBlinkdurationAsync():
     if request.method == 'POST':
        body = request.json
        key = body['key']
        url_link = request.args['url']
        print(url_link)
        uncodeURL = unquote(url_link)
        parseURL = urlparse(uncodeURL)
        videoName = os.path.basename(parseURL.path)
        urllib.request.urlretrieve(url_link,os.path.join(DOWNLOAD_FOLDER,videoName))
        json_dict = {}
        total , duration , timer = await timeProcess(videoName)
        status = ''
        if total == 0:
            status = 'Not Eye Detected'
        else:
            if duration > 30:
                status = 'too long video'
            elif duration == 30:
                status = 'OK video'
            else: 
                status = 'too short video'

        print('interval time : ' + str(timer) )
        print('total blink : ' + str(total) )
        print('status : ' + str(status))
        firebase = Firebase(config)
        data = {
            u'name':videoName, u'duration':timer, u'status':status,
        }
        valueList['IntervalTime'] = timer 
        try:
            db.collection(u'dryeye').document(key).update(data)
        except:
            db.collection(u'dryeye').document(key).set(data)
        return 'IntervalTime Success'
 
@app.route('/returnMock')
def returnMock():
    mock = {
        "BlinkFrequency": 2,
        "IntervalTime" : 2
    }
    mockJSON = json.dumps(mock)
    return mockJSON

@app.route('/dataMock')
def dataMock():
    valueList['IntervalTime'] = '99'
    valueList['BlinkFrequency'] = '99'
    return 'Mock Success'


async def checkNull():
    while (valueList['IntervalTime'] == '' or  valueList['BlinkFrequency'] == ''):
        print('null')
    print('data add complete')
 

@app.route('/returnValueLoop')
async def returnValueLoop():
    await checkNull()
    valueJSON = json.dumps(valueList)
    return valueJSON

@app.route('/returnValue')
async def returnValue():
    valueJSON = json.dumps(valueList)
    return valueJSON
    
@app.route('/returnValueBlink')
async def returnValueBlink():
    valueJSON = json.dumps(valueList['BlinkFrequency'])
    return valueJSON

@app.route('/returnValueTime')
async def returnValueTime():
    valueJSON = json.dumps(valueList['IntervalTime'])
    return valueJSON

@app.route('/clearValue')
def clearValue():
    valueList['IntervalTime'] = ''
    valueList['BlinkFrequency'] = ''
    return 'clear value success'
    
@app.route('/valueEyeBlink')
def valueEyeBlink():
    #if(request.headers.get('key')==secret_key):
    json_dict = {}
    #storage.child("video_mockup/test.mp4").download(os.path.join(DOWNLOAD_FOLDER,'mockup.mp4'))
    value = eyeblink.eyeblink('5.mp4')
    firebase = Firebase(config)
    db = firestore.Client()
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    data = {
        'name':'test', 'result':value, 'time':date_time
    }
    db.collection(u'dryeye').document(u'eyeblink').set(data)
    
        #eyeblink.clearFolder()
    return 'eyeblink update'


@app.route('/valueBlinkDuration')
def valueBlinkDuration():
    #if(request.headers.get('key')==secret_key):
    json_dict = {}
    #storage.child("video_mockup/test.mp4").download(os.path.join(DOWNLOAD_FOLDER,'mockup.mp4'))
    value = blinkduration.blinkduration()
        #eyeblink.clearFolder()
    db = firestore.Client()
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    data = {
        'name':'test', 'result':value, 'time':date_time
    }
    db.collection(u'dryeye').document(u'blinkduration').set(data)
    
        #eyeblink.clearFolder()
    return 'blinkduration update'

@app.route('/clearFile')
def clearFile():
     
    return 'Clear File Complete'

@app.route('/checkFile')
def checkFile():
    list = eyeblink.checkFolder()
    return jsonify(list)

if __name__ == "__main__":
    app.run(debug=False)