import mysql.connector
import cv2
import pickle
import numpy as np
import matplotlib.pyplot as plt
import dlib
from datetime import datetime


class Detector():

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")
    face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer/train.yml")
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Creating a list eye_blink_signal
    eye_blink_signal=[]
    # Creating an object blink_ counter
    blink_counter = 0
    previous_ratio = 100
    # Creating a while loop

    labels = {"person_name": 1}
    with open("labels.pickle", "rb") as f:
        labels = pickle.load(f)
        labels = {v: k for k, v in labels.items()}

    #koneksi Database
    myconn = mysql.connector.connect(host="localhost", user="root", passwd="", database="facerecognition")
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    cursor = myconn.cursor()

    def __init__(self):
        
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 640) # set video widht
        self.cam.set(4, 480) # set video height

        if not self.cam.isOpened():
            print("Unable to connect to camera.")
            return
        while self.cam.isOpened():
            self.ret, self.frame = self.cam.read()
            self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            self.faceRec = self.face_cascade.detectMultiScale(self.gray, scaleFactor=1.5, minNeighbors=5)
            for (x, y , w, h) in self.faceRec:
                self.faces = self.detector(self.gray)
                for face in self.faces:
                    self.roi_gray = self.gray[y:y + h, x:x+ w]
                    self.roi_color = self.frame[y:y + h, x:x+ w]
                    self.id_, self.confidence = self.recognizer.predict(self.gray[y:y+h,x:x+w])

                    x, y = face.left(), face.top()
                    x1, y1 = face.right(), face.bottom()
                    # Creating an object in which we will sore detected facial landmarks
                    self.landmarks = self.predictor(self.gray, face)
                    # Calculating left eye aspect ratio    
                    self.left_eye_ratio = self.get_EAR([36, 37, 38, 39, 40, 41], self.landmarks)
                    # Calculating right eye aspect ratio  
                    self.right_eye_ratio = self.get_EAR([42, 43, 44, 45, 46, 47], self.landmarks)
                    # Calculating aspect ratio for both eyes  
                    self.blinking_ratio = (self.left_eye_ratio + self.right_eye_ratio) / 2
                    # Rounding blinking_ratio on two decimal places   
                    self.blinking_ratio_1 = self.blinking_ratio * 100
                    self.blinking_ratio_2 = np.round(self.blinking_ratio_1)
                    self.blinking_ratio_rounded = self.blinking_ratio_2 / 100


                    # Appending blinking ratio to a list eye_blink_signal
                    self.eye_blink_signal.append(self.blinking_ratio)
                    if self.blinking_ratio < 0.20:
                        if self.previous_ratio > 0.20:
                            self.blink_counter = self.blink_counter + 1
                    # Displaying blink counter and blinking ratio in our output video          
                    self.previous_ratio = self.blinking_ratio

                    if(self.blink_counter == 0):
                        self.message = "Kedipkan mata"
                    elif(self.blink_counter < 2):
                        self.message = "kedipkan mata Lagi"
                    elif(self.blink_counter > 2):
                        self.message ="Posisi kurang Benar"

                    if (self.confidence < 100 ):
                        
                        self.name = self.labels[self.id_]
                        self.syncron = "  {0}%".format(round(100 - self.confidence))
                        if(((100 - self.confidence) > 45) and (self.blink_counter >= 3)):
                            self.sql = "INSERT INTO absen (nama,tanggal, waktu) VALUES (%s, %s, %s)"
                            self.val = (self.name,self.current_date, self.current_time)
                            self.cursor.execute(self.sql, self.val)
                            self.myconn.commit()
                            from tkinter import messagebox
                            self.response = messagebox.showinfo("Info Absen" ,"Terimakasih Anda telah Absen")
                            if self.response == "ok":
                                self.close()
                    else:
                        self.name = "unknown"
                        self.syncron = "  {0}%".format(round(100 - self.confidence))

                    
                    cv2.putText(self.frame, str(self.blink_counter), (30, 50), self.font, 2, (0, 0, 255),5)
                    cv2.putText(self.frame, str(self.blinking_ratio_rounded), (900, 50), self.font, 2, (0, 0, 255),5)
                    cv2.putText(self.frame, self.message, (x+5,y+h+20), self.font, 1, (0,0,255), 3)
                    cv2.rectangle(self.frame, (x, y), (x+ w, y + h), (255, 0, 0), (2))
                    cv2.rectangle(self.frame,(x,y-37),(x+w,y),(255,0,0),-2)
                    cv2.putText(self.frame, self.name, (x, y-10),self.font,1,(255,255,255),2)
                    cv2.putText(self.frame, str(self.syncron), (x+100, y-10),self.font,1,(255,255,255),2)
        
                    cv2.imshow('Face Detection', self.frame)
            self.k = cv2.waitKey(20) & 0xff
            if self.k == ord('q'):
                break
                
        print("\n [INFO] Exiting Program and cleanup stuff")
        self.close()

    def midpoint(self,p1 ,p2):
        return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

    # Defining the Euclidean distance
    def euclidean_distance(self,leftx,lefty, rightx, righty):
        return np.sqrt((leftx-rightx)**2 +(lefty-righty)**2)

    # Defining the eye aspect ratio
    def get_EAR(self,eye_points, facial_landmarks):
        # Defining the left point of the eye   
        self.left_point = [facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y]
        # Defining the right point of the eye   
        self.right_point = [facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y]
        # Defining the top mid-point of the eye    
        self.center_top = self.midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
        # Defining the bottom mid-point of the eye   
        self.center_bottom = self.midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
        # Drawing horizontal and vertical line       
        hor_line = cv2.line(self.frame, (self.left_point[0], self.left_point[1]), (self.right_point[0], self.right_point[1]), (255, 0, 0), 3)
        self.ver_line = cv2.line(self.frame, (self.center_top[0], self.center_top[1]),(self.center_bottom[0], self.center_bottom[1]), (255, 0, 0), 3)
        # Calculating length of the horizontal and vertical line    
        hor_line_lenght = self.euclidean_distance(self.left_point[0], self.left_point[1], self.right_point[0], self.right_point[1])
        self.ver_line_lenght = self.euclidean_distance(self.center_top[0], self.center_top[1], self.center_bottom[0], self.center_bottom[1])
        # Calculating eye aspect ratio     
        self.EAR = self.ver_line_lenght / hor_line_lenght
        return self.EAR

    def close(self):
        self.cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    Detector()
    