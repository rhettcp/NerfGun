import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

ledPin = 17

print 'blue'
GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(ledPin, GPIO.HIGH)
time.sleep(1)

print 'yellow'
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, GPIO.HIGH)

time.sleep(2)
    
GPIO.cleanup()
