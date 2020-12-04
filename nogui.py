
from __future__ import division
import time
from time import sleep
import numpy as np
import cv2 #
import pygame
import pigpio

#-----------------------------------------------------------------------------------------------------

music_count = 0

music_file = "/home/pi/Desktop/gi/gi/sound/inform_voice.mp3"

Folder = '/home/pi/Desktop/gi/gi/'

NOFACE_MAX = 23
MUSIC_START = 5

noface_count = 0

dg_x = 90
dg_y = 110

BASE_DEGREE = 600
SUB_ANGLE = 10

degree_x = 600
degree_y = 600

MIN_ANGLE_x = 5
MAX_ANGLE_x =175
MIN_ANGLE_y = 90
MAX_ANGLE_y =175

COLOR_BLUE = (255,0,0)
COLOR_GREEN = (0, 255, 0)

midfaceY=0
midfaceX=0

midscreenY=(480/2)
midscreenX=(640/2)
midscreenwindow = 50
stepsize_x = 3
stepsize_y = 2

#------------------------------------------------------------------------------------------------------------------------
pi = pigpio.pi()


pi.set_servo_pulsewidth(18, 1500) #reset servo position first
pi.set_servo_pulsewidth(23, 1600) #y axis

faceCascade = cv2.CascadeClassifier(Folder + 'haarcascade_frontalface_default.xml') #set frontal face
profaceCascade = cv2.CascadeClassifier(Folder + 'haarcascade_profileface.xml') # set profile face


cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height


pygame.mixer.init(48000,-16,1,1024) #init mixer (samplerate,bit,channel,buffersize)
pygame.mixer.music.load(music_file) # load music file

while True:
    #first  detection

    ret, img = cap.read()
    img = cv2.flip(img, 0)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2,minNeighbors=5,minSize=(40, 40),maxSize=(400,400))
    
    
    
    if not len(faces) :
        faces = profaceCascade.detectMultiScale(gray, scaleFactor=1.2,minNeighbors=5,minSize=(40, 40),maxSize=(400,400))
        #if there is no frontalface
        
        
    if len(faces) > 0 : #exists face
        
        noface_count = 0
        music_count += 1

        #print("there are",len(faces),"faces in this video")
        
        if not pygame.mixer.music.get_busy() and music_count > MUSIC_START :
            
            
            pygame.mixer.music.play()

        
        max_face = faces[0]
        max_w = max_face[2]

        #many faces case
        for (x,y,w,h) in faces :
            if w > max_w:
                max_face = (x,y,w,h)
                max_w = w

        x,y,w,h = max_face
        #cv2.rectangle(img,(x,y),(x+w,y+h),COLOR_BLUE,3)




        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]



        if w > 0 :

            midfaceX = x + (w/2)
            midfaceY = y + (h/2)


            if midfaceY < (midscreenY - midscreenwindow) :

                if dg_y >= MIN_ANGLE_y and dg_y <= MAX_ANGLE_y - stepsize_y  :
                    dg_y += stepsize_y


            elif midfaceY > (midscreenY + midscreenwindow) :

                if dg_y <= MAX_ANGLE_y and dg_y >= MIN_ANGLE_y + stepsize_y :
                    dg_y -= stepsize_y



            if midfaceX < (midscreenX - midscreenwindow) :

                if dg_x >= MIN_ANGLE_x and dg_x <= MAX_ANGLE_x - stepsize_x  :
                    dg_x -= stepsize_x


            elif midfaceX > (midscreenX + midscreenwindow) :

                if dg_x <= MAX_ANGLE_x and dg_x >= MIN_ANGLE_x + stepsize_x:
                    dg_x += stepsize_x
                    
        
        


    else :
        

        music_count = 0
        
        if noface_count > NOFACE_MAX :
            
            #print('no face during 3s. stop music')
            
            dg_y -= ((dg_y-110)/16)
            dg_x -= ((dg_x-90)/16)
            

        
            pygame.mixer.music.stop()
            
        else :
            
            noface_count += 1
        
    
    pi.set_servo_pulsewidth(23, BASE_DEGREE + SUB_ANGLE*(dg_y)) # control servo y
    pi.set_servo_pulsewidth(18, BASE_DEGREE + SUB_ANGLE*(dg_x)) # control servo x


    #cv2.imshow('video', img) #show video
    #k = cv2.waitKey(1) & 0xff
    
    #if k == 27: # press 'ESC' to quit
    #    pi.set_servo_pulsewidth(23, 1600) #reset servo position
     #   pi.set_servo_pulsewidth(18, 1500)

     #   break


pi.set_servo_pulsewidth(23, 0) #release servo power
pi.set_servo_pulsewidth(18, 0)

cap.release()
#cv2.destroyAllWindows()
