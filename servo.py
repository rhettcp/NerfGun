from Tkinter import *
import RPi.GPIO as GPIO
import time

current = 90
minTrigger = 85
maxTrigger = 150

#Helpers
def xToAngle(x):
    return x

def yToAngle(y):
    return y

def moveServo(servo, angle):
    duty = float(angle) / 10.0 + 2.5
    servo.ChangeDutyCycle(duty)
    print angle, duty

#Main Functions

def moveNerfGun(panServo, tiltServo, x, y):
    moveServo(panServo, xToAngle(x))
    moveServo(tiltServo, yToAngle(y))

def fireNerfDart(trigger):
    triggerAng = minTrigger
    moveServo(trigger, minTrigger)
    while(triggerAng < maxTrigger):
	moveServo(trigger, triggerAng)
	triggerAng += 1
	time.sleep(0.008)
    while(triggerAng > minTrigger):
	moveServo(trigger, triggerAng)
	triggerAng -= 1
	time.sleep(0.004)

#Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

trigger = GPIO.PWM(18, 100)
pan = GPIO.PWM(20, 100)
tilt = GPIO.PWM(21, 100)

trigger.start(5)
pan.start(5)
tilt.start(5)

#Main
fireNerfDart(trigger)
