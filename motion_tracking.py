import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

camera = cv2.VideoCapture(0)
GPIO.setmode(GPIO.BCM)

target = (460, 236)

fire_pin = 23
motor_pin = 17
fire_displacement = 50

firstFrame = None
previousFrame = None

GPIO.setup(fire_pin, GPIO.OUT)
GPIO.setup(motor_pin, GPIO.OUT)

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
    firing = False

    if not contours:
        GPIO.output(motor_pin, GPIO.LOW)
    else:
        GPIO.output(motor_pin, GPIO.HIGH)
    for c in contours:
        if cv2.contourArea(c) < 3500:
            continue
        hasContour = True
        (x,y,w,h) = cv2.boundingRect(c)
        center = (x + w /2, y + h/4)
        cv2.rectangle(frame, (x,y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(frame, center, 10, (0,0,255), thickness=2)
        difference = np.sqrt((target[0] - center[0])**2 + (target[1] - center[1])**2)
        if (difference < fire_displacement):
            firing = True

    if firing:
        GPIO.output(fire_pin, GPIO.HIGH)
    else:
        GPIO.output(fire_pin, GPIO.LOW)

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

GPIO.cleanup()
camera.release()
cv2.destroyAllWindows()
