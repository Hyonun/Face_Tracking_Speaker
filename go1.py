from __future__ import division
import time
from time import sleep
import numpy as np
import cv2
PI = False

if PI:
    import pigpio

    pi = pigpio.pi()

    pi.set_servo_pulsewidth(18, 0)
    pi.set_servo_pulsewidth(23, 0)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

dg_x = 90
dg_y = 90

MIN_ANGLE = 5
MAX_ANGLE =175

midfaceY=0
midfaceX=0

midscreenY=(SCREEN_HEIGHT/2)
midscreenX=(SCREEN_WIDTH/2)
midscreenwindow = 40
stepsize_x = 3
stepsize_y = 2

#haarcascade_frontalface_default.xml
faceCascade = cv2.CascadeClassifier('/harr/haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
cap.set(3,SCREEN_WIDTH) # set Width
cap.set(4,SCREEN_HEIGHT) # set Height

tracking_control = 1

while True:
    #first all windows detection
    if tracking_control == 1 :

        ret, img = cap.read()
        img = cv2.flip(img, 0)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


        faces = faceCascade.detectMultiScale(gray,
                                             scaleFactor=1.2,
                                             minNeighbors=5,
                                             minSize=(40, 40))

        if len(faces) > 0 :
            # x,y,w,h = faces[0]
            # many faces case
            for x,y,w,h in faces :
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),3)

        #second closely face detection
        #make fuction and localizing

        #
         #   cropped = img[y - int(h/4):y + h + int(h/4), x - int(w/4):x + w + int(w/4)]
         #   cropped_gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
         #   faces_near = faceCascade.detectMultiScale(
      # cropped_gray,scaleFactor=1.2,minNeighbors=5,minSize=(40, 40))

            if w > 0 :

                midfaceX = x + (w/2)
                midfaceY = y + (h/2)

                print('center faceX : ', midfaceX)
                print('center faceY : ', midfaceY)
                print(' before dg_x : ', dg_x)
                print(' before dg_x : ', dg_y,"\n")


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


        print('realX degree : ', dg_x)
        print('realY degree : ', dg_y)


        degree_x = 600 + 10*(dg_x)
        degree_y = 600 + 10*(dg_y)

        print('after X : ', degree_x)
        print('after Y : ', degree_y,"\n")

        if PI:
            pi.set_servo_pulsewidth(18, 0)
            pi.set_servo_pulsewidth(23, 0)
            pi.set_servo_pulsewidth(18, degree_y) # position anti-clockwise
            pi.set_servo_pulsewidth(23, degree_x) # position anti-clockwise
        sleep(0.015)


        cv2.imshow('video', img) #
        k = cv2.waitKey(1) & 0xff
    if k == 27: # press 'ESC' to quit
        if PI:
            pi.set_servo_pulsewidth(23, 1500)
            pi.set_servo_pulsewidth(18, 1500)
        break


if PI:
    pi.set_servo_pulsewidth(23, 0)
    pi.set_servo_pulsewidth(18, 0)

cap.release()
cv2.destroyAllWindows()
