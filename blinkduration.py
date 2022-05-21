import os 
import cv2
import dlib
from scipy.spatial import distance
from imutils import face_utils
import time
import math

#parameter
count = 0
total = 0
eye_check = 0.2 #0.275
count_min = 3


APP_FOLDER = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(APP_FOLDER,'download')



#second
#cap = cv2.VideoCapture(os.path.join(DOWNLOAD_FOLDER,video_list[len(video_list)-1]))

 
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    eye = (A + B) / (2.0 * C)
    return eye
 

def blinkduration (name):
    cap = cv2.VideoCapture(os.path.join(DOWNLOAD_FOLDER,name))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps
    duration = math.floor(duration)
    frame_init = 0
    seconds = time.time() 
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('rsc/shape_predictor_68_face_landmarks.dat')
    count = 0
    total = 0
    while True:
        success,img = cap.read()
        imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = detector(imgGray)
 
        for face in faces:
            landmarks = predictor(imgGray,face)
 
            landmarks = face_utils.shape_to_np(landmarks)
            leftEye = landmarks[42:48]
            rightEye = landmarks[36:42]
 
            leftEye = eye_aspect_ratio(leftEye)
            rightEye = eye_aspect_ratio(rightEye)
            eye = (leftEye + rightEye) / 2.0      

            if eye<eye_check:
                count+=1
            else:
                if count>=count_min:
                    print(eye)
                    total+=1
                count=0

        frame_init = frame_init + 1
        timer = math.floor(frame_init/fps)
        print('timer by frame : ' + str(timer))
        countdown = duration-timer
        print('countdown : ' + str(countdown))
        if total != 0 or countdown == 0 or timer == 30:
	        return total , duration , timer

def clearFolder():
    for f in os.listdir(DOWNLOAD_FOLDER):
        if not f.endswith(".mp4"):
            continue
    os.remove(os.path.join(DOWNLOAD_FOLDER, f))
  