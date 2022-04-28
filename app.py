import os

from flask import Flask, jsonify, request, render_template, Response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import requests
import cv2
import eyeblink
import blinkduration
from firebase import Firebase 


config = {
  "apiKey": "AIzaSyC23zle1HEwFlNQOi10E4QdTLtdiLkIsb0",
  "authDomain": "dryeye-video-firebase.firebaseapp.com",
  "databaseURL": "https://dryeye-video-firebase-default-rtdb.asia-southeast1.firebasedatabase.app",
  "storageBucket": "dryeye-video-firebase.appspot.com",
  "serviceAccount" : "dryeye-video-firebase-firebase-adminsdk-rpf9i-4f393863ef.json"
}

app = Flask(__name__)
app.config.from_object(__name__)
secret_key = '569b9653d72565a63435e873bbab94ed'
#569b9653d72565a63435e873bbab94ed
app.config['SECRET_KEY'] = secret_key

APP_FOLDER = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(APP_FOLDER,'upload')

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


@app.route('/downloadVideo')
def downloadVideo():
    # if request.method == 'GET':
    #     if(request.headers.get('key')==secret_key):
    firebase = Firebase(config)
    storage = firebase.storage()
    storage.child("video_mockup/test.mp4").download("download/mockup.mp4")
    return 'video uploaded successfully'
    # else:
    #     return 'failed'


@app.route('/uploader')
def uploader():
    f = request.files['filename']
    f.save(os.path.join (app.config['UPLOAD_FOLDER'],f.filename))
    return 'file uploaded successfully'


@app.route('/valueEyeBlink')
def valueEyeBlink():
    #if(request.headers.get('key')==secret_key):
    json_dict = {}
    value = eyeblink.eyeblink()
        #eyeblink.clearFolder()
    return str(value)


@app.route('/valueBlinkDuration')
def valueBlinkDuration():
    #if(request.headers.get('key')==secret_key):
    json_dict = {}
    value = blinkduration.blinkduration()
        #eyeblink.clearFolder()
    return str(value)



if __name__ == "__main__":
    app.run(debug=False)