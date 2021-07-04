import imutils
import cv2, os
import numpy as np
from django.conf import settings
from imutils import face_utils
import dlib
from imutils.video import VideoStream
from scipy.spatial import distance
from pygame import mixer
mixer.init()
sound = mixer.Sound("livestream/alarm.wav")


# Load facial landmark predictor from dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("livestream/shape_predictor_68_face_landmarks.dat")




# Using only a threshold value for detecting drowsiness
EYE_THRESH = 0.25  #indicate for blink
EYE_FRAMES = 40  #minimum of consecutive frames of blinking
FRAME_COUNTER = 0

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        #success,imgNp = self.url.read()
        #resize = cv2.resize(imgNp, (640, 480), interpolation = cv2.INTER_LINEAR)
        _, image = self.video.read()
        image = imutils.resize(image, width=450)
        # Convert img to grayscale
        frame_flip = cv2.flip(image,1)
        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        return jpeg.tobytes()

class eyedet(object):
    def __init__(self):
        self.video = VideoStream(src=0).start()
        

    def __del__(self):
        cv2.destroyAllWindows()

    def eye_aspect_ratio(self, eye):
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])
        C = distance.euclidean(eye[0], eye[3])
        ear = (A+B) / (2.0 * C)
        #print("hi")
        return ear

    def get_frame(self, FRAME_COUNTER = 0):
        EYE_THRESH = 0.30  #indicate for blink
        EYE_FRAMES = 40  #minimum of consecutive frames of blinking
        
        #success,imgNp = self.url.read()
        #resize = cv2.resize(imgNp, (640, 480), interpolation = cv2.INTER_LINEAR)
        image = self.video.read()
        image = imutils.resize(image, width=720)
        
        frame_flip = cv2.flip(image,1)
        gray = cv2.cvtColor(frame_flip, cv2.COLOR_BGR2GRAY)
        # detect faces in the grayscaled frame
        rects = detector(gray, 0)
        for rect in rects:
        # get facial landmarks for the face region and convert to np array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            # build features 
            eye = shape[36:68] # Extracting relevant parts (eyes to mouth)
            ear = self.eye_aspect_ratio(eye)
            # visualize contours only of the eyes
            leftEye  = shape[42:48]
            rightEye = shape[36:42]
            cv2.drawContours(frame_flip, [cv2.convexHull(leftEye)], -1, (0, 255, 0), 1)
            cv2.drawContours(frame_flip, [cv2.convexHull(rightEye)], -1, (0, 255, 0), 1)

            #check if ear is below defined threshold
            if ear < EYE_THRESH:
                FRAME_COUNTER = FRAME_COUNTER + 1
                print(FRAME_COUNTER)
                if FRAME_COUNTER >= EYE_FRAMES:
                    cv2.putText(frame_flip, "Drowsiness detected!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    sound.play()
                    
                    #cv2.putText(image, Result_String, bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            else:
                FRAME_COUNTER = 0
                print(FRAME_COUNTER)
            
            #draw EAR
            cv2.putText(frame_flip, "EAR: {:3f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        return (jpeg.tobytes(), FRAME_COUNTER)