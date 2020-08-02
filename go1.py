
from __future__ import division
import time
from time import sleep
import numpy as np
import cv2 #
#import pigpio

#pi = pigpio.pi()

#pi.set_servo_pulsewidth(18, 0)
#pi.set_servo_pulsewidth(23, 0)

dg_x = 90
dg_y = 90

MIN_ANGLE = 5
MAX_ANGLE =175


midfaceY=0
midfaceX=0

midscreenY=(480/2)
midscreenX=(640/2)
midscreenwindow = 40
stepsize_x = 3
stepsize_y = 2

#p.ChangeDutyCycle(degree_y)
#p1.ChangeDutyCycle(degree_x)



#haarcascade_frontalface_default.xml
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

tracking_control = 1

while True:
    #first all windows detection
    if tracking_control == 1 :
    
    
        ret, img = cap.read()
        #img = cv2.flip(img, 0)  
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2,minNeighbors=5,minSize=(40, 40),maxSize=(400,400))
    
    
        if len(faces) > 0 :
                  
        
           #many faces case
            for (x,y,w,h) in faces :
                x1,y1,w1,h1 = faces[0]
                cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),3)

                if len(faces) > 1 :
                    x2,y2,w2,h2 = faces[1]

                    if w2 < w1 :
                        cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(0,255,0),3)

        
    
                
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
        
        
    
            if w > 0 :
            
                midfaceX = x + (w/2)
                midfaceY = y + (h/2)
            
                print('center faceX : ', midfaceX)
                print('center faceY : ', midfaceY)
                print(' face_width : ', w)
                print(' face_length : ', h,"\n")
            
            
                if midfaceY < (midscreenY - midscreenwindow) :
                
                    if dg_y >= MIN_ANGLE and dg_y <= MAX_ANGLE-stepsize_y  :
                        dg_y += stepsize_y
            
            
                elif midfaceY > (midscreenY - midscreenwindow) :
    
                    if dg_y <= MAX_ANGLE and dg_y >= MIN_ANGLE + stepsize_y :
                        dg_y -= stepsize_y
            
  
            
                if midfaceX < (midscreenX - midscreenwindow) :
                
                    if dg_x >= MIN_ANGLE and dg_x <= MAX_ANGLE-stepsize_x  :
                        dg_x += stepsize_x
            
            
                elif midfaceX > (midscreenX - midscreenwindow) :
                
                    if dg_x <= MAX_ANGLE and dg_x >= MIN_ANGLE + stepsize_x:
                        dg_x -= stepsize_x
                    
            
        
        degree_x = 600 + 10*(dg_x)
        degree_y = 600 + 10*(dg_y)
        
        print('no faces')
    
   # pi.set_servo_pulsewidth(18, 0)
    #pi.set_servo_pulsewidth(23, 0) 
       # pi.set_servo_pulsewidth(18, degree_y) # position anti-clockwise
        #pi.set_servo_pulsewidth(23, degree_x) # position anti-clockwise
        sleep(0.015)

        
        cv2.imshow('video', img) # 
        k = cv2.waitKey(1) & 0xff
    if k == 27: # press 'ESC' to quit 
        #pi.set_servo_pulsewidth(23, 1500)
        #pi.set_servo_pulsewidth(18, 1500)
        
        break
    
    
#pi.set_servo_pulsewidth(23, 0)
#pi.set_servo_pulsewidth(18, 0)

cap.release()
cv2.destroyAllWindows()
