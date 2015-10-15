import argparse
import datetime
import time
import cv2
import numpy as np

camera = cv2.VideoCapture(0)

target = (460, 236)

firstFrame = None
previousFrame = None

counter = 0
interval = 2
while(True):
    hasContour = False
    grabbed, frame = camera.read()
    if not grabbed:
        print 'exiting'
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if firstFrame is None:
        firstFrame = gray
        continue
    frameDelta = cv2.absdiff(firstFrame, gray)

    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=2)
    (contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) < 3500:
            continue
        hasContour = True
        (x,y,w,h) = cv2.boundingRect(c)
        center = (x + w /2, y + h/4)
        print center
        cv2.rectangle(frame, (x,y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(frame, center, 10, (0,0,255), thickness=2)
        difference = np.sqrt((target[0] - center[0])**2 + (target[1] - center[1])**2)
        if (difference < 25):
            print 'firing' 

    if previousFrame is not None:
        previousDelta = cv2.absdiff(previousFrame, gray)
        if np.sum(previousDelta) < 100000 and counter % interval == 0:
            firstFrame = previousFrame
            interval = interval*2
            print 'reset'


    cv2.imshow('frame', frame)
    cv2.imshow('thresh', thresh)
    cv2.imshow('delta', frameDelta)
    cmd = cv2.waitKey(1) & 0xFF
    if cmd == ord('q'):
        break
    elif cmd == ord('k'):
        firstFrame = gray
    previousFrame = gray    
    counter += 1
camera.release()
cv2.destroyAllWindows()
