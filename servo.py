from Tkinter import *
import RPi.GPIO as GPIO
import time

current = 90

def moveServo(servo, angle):
    duty = float(angle) / 10.0 + 2.5
    servo.ChangeDutyCycle(duty)
    print angle, duty

def fireNerfDart(trigger):
    triggerAng = 60
    while(triggerAng < 130):
	moveServo(trigger, triggerAng)
	triggerAng += 1
	time.sleep(0.008)
    moveServo(trigger, 60)   


GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)

pan = GPIO.PWM(18, 100)
trigger = GPIO.PWM(20, 100)

pan.start(5)
trigger.start(5)

moveServo(pan, 90)
moveServo(trigger, 60)

fireNerfDart(trigger)




