import cv2
import numpy as np 
import time
import os
from tkinter import *

class Generat():
   
    h, w = 480, 640
    black = np.zeros((h,w,3), dtype=np.uint8)
    foto = black

    #image frame
    ymin, ymax = h//2 - 125, h//2 + 125
    xmin, xmax = w//2 - 125, w//2 + 125

    n_image = 1
    capture_delay = 2 # second

    filename = ''
    label_frame = ''

    cam = cv2.VideoCapture(0)
    

    last_time = time.time()

    def __init__(self,name,count):
        self.name = str(name)
        self.max_image = int(count)
        os.makedirs('dataset/'+self.name)
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3,self.w)
        self.cam.set(4,self.h)
        if not self.cam.isOpened():
            print("Unable to connect to camera.")
            return
        while self.cam.isOpened():
            try :
                self.ret, self.frame = self.cam.read()
                if self.filename == '' and (time.time() - self.last_time):
                    self.label_frame = 'Next Capture in ' + str(int(self.capture_delay - (time.time() - self.last_time)))
                else :
                   self.label_frame = self.filename
                
                self.frame = self.box(self.frame)
                
                cv2.imshow('frame',np.hstack((self.frame, self.foto)))
                
                if (time.time() - self.last_time) > self.capture_delay :
                    self.last_time = time.time()
                    self.filename = 'dataset/%s' % self.name + '/'+ str(self.n_image) + ".jpg"
                    self.n_image = self.n_image + 1
                    self.foto[self.ymin:self.ymax, self.xmin:self.xmax] = self.frame[self.ymin:self.ymax, self.xmin:self.xmax]
                    
                    cv2.imwrite(self.filename, self.frame[self.ymin:self.ymax, self.xmin:self.xmax])
                    print(self.filename, " saved!")
                    
                if (time.time() - self.last_time) > self.capture_delay*0.25 :
                    self.foto = self.black
                    self.filename = ""

                if (cv2.waitKey(1) & 0xFF == ord('q')) or (self.n_image >= self.max_image):
                    self.close()
                    
                    
            except Exception as e: 
                print(e)     
                self.close()

    def close(self):
        self.cam.release()
        cv2.destroyAllWindows()
        
    def box(self,img):
        cv2.rectangle(img, (self.xmin-1, self.ymin-21), (self.xmax+1, self.ymin-1), (0,255,0),-1)
        cv2.putText(img, self.label_frame, (self.xmin+6, self.ymin-4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)  
        cv2.rectangle(img,(self.xmin-1, self.ymin-1),(self.xmax+1, self.ymax+1),(0,255,0),1)
        cv2.rectangle(img, (self.xmin-1, self.ymax+1), (self.xmax+1, self.ymax+26), (0,255,0),-1)
        cv2.putText(img, "posisikan wajah pada bingkai..", 
                    (self.xmin+6, self.ymax+16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1) 
        return img

  