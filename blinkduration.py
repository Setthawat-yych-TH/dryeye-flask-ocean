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
eye_check = 0.3 #0.275
count_min = 2
count_max = 5 


APP_FOLDER = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(APP_FOLDER,'download')


video_list = []
for fname in os.listdir(DOWNLOAD_FOLDER):
    if fname.endswith('.mp4'):
        print(fname)
        video_list.append(fname)
        break
    else: print('not used')

#second
#cap = cv2.VideoCapture(os.path.join(DOWNLOAD_FOLDER,video_list[len(video_list)-1]))
cap = cv2.VideoCapture(os.path.join(DOWNLOAD_FOLDER,'mockup.mp4'))
seconds = time.time() 
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('rsc/shape_predictor_68_face_landmarks.dat')
 
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    eye = (A + B) / (2.0 * C)
    return eye
 

def blinkduration ():
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
                if not(leftEye > 0.25 and rightEye > 0.25):
                    count+=1
                #0.275 1214,12.14
            else:
                if count>=count_min and count <=count_max:
                    print(eye)
                    total+=1

        timer = math.floor(time.time()-seconds)
        #cv2.imshow('Video',img)
        if cv2.waitKey(5) & 0xFF == ord('q') or total == 1:
	        return timer

def clearFolder():
    for f in os.listdir(DOWNLOAD_FOLDER):
        if not f.endswith(".mp4"):
            continue
    os.remove(os.path.join(DOWNLOAD_FOLDER, f))
  