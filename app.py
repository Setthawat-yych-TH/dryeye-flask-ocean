import os

from numpy import eye

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
  "apiKey": "AIzaSyC23zle1HEwFlNQOi10E4QdTLtdiLkIsb0",
  "authDomain": "dryeye-video-firebase.firebaseapp.com",
  "databaseURL": "https://dryeye-video-firebase-default-rtdb.asia-southeast1.firebasedatabase.app",
  "storageBucket": "dryeye-video-firebase.appspot.com",
  "serviceAccount" : "dryeye-video-firebase-firebase-adminsdk-rpf9i-4f393863ef.json"
}

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dryeye-video-firebase-firebase-adminsdk-rpf9i-64aa3ea14e.json"
cred = credentials.Certificate("dryeye-video-firebase-firebase-adminsdk-rpf9i-64aa3ea14e.json")
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


@app.route('/downloadURL', methods= ['post'])
def downloadURL():
    if request.method == 'POST':
        url_link = request.args['url']
    #https%3A%2F%2Ffirebasestorage.googleapis.com%2Fv0%2Fb%2Feye-examination-database.appspot.com%2Fo%2Ffiles%252FREC2570387848447835707.mp4%3Falt%3Dmedia%26token%3D93d5ef70-0b18-41db-b915-a91539a3a453
        print(url_link)
        urllib.request.urlretrieve(url_link,os.path.join(DOWNLOAD_FOLDER,'mockup_url.mp4'))
        return 'video downloaded successfully' 

@app.route('/eyeblink', methods=['POST'])
def getEyeblink():
     if request.method == 'POST':
        url_link = request.args['url']
        print(url_link)
        uncodeURL = unquote(url_link)
        parseURL = urlparse(uncodeURL)
        videoName = os.path.basename(parseURL.path)
        urllib.request.urlretrieve(url_link,os.path.join(DOWNLOAD_FOLDER,videoName))
        json_dict = {}
        value = eyeblink.eyeblink(videoName)
        firebase = Firebase(config)
        cred = credentials.Certificate("dryeye-video-firebase-firebase-adminsdk-rpf9i-64aa3ea14e.json")
        firebase_admin.initialize_app(cred)
        db = firestore.Client()
        data = {
            'name':videoName, 'result':value, 
        }
        db.collection(u'eyeblink').document(videoName).set(data)
        return 'video uploaded successfully'

        
@app.route('/blinkduration', methods=['POST'])
def getBlinkduration():
     if request.method == 'POST':
        url_link = request.args['url']
        print(url_link)
        uncodeURL = unquote(url_link)
        parseURL = urlparse(uncodeURL)
        videoName = os.path.basename(parseURL.path)
        urllib.request.urlretrieve(url_link,os.path.join(DOWNLOAD_FOLDER,videoName))
        json_dict = {}
        value = blinkduration.blinkduration(videoName)
        firebase = Firebase(config)
        cred = credentials.Certificate("dryeye-video-firebase-firebase-adminsdk-rpf9i-64aa3ea14e.json")
        firebase_admin.initialize_app(cred)
        db = firestore.Client()
        data = {
            'name':videoName, 'result':value, 
        }
        db.collection(u'blinkduration').document(videoName).set(data)
        return 'video uploaded successfully'
 

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
    eyeblink.clearFolder()
    return 'Clear File Complete'

@app.route('/checkFile')
def checkFile():
    list = eyeblink.checkFolder()
    return jsonify(list)

if __name__ == "__main__":
    app.run(debug=False)