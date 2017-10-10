# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

GPIO.setup(12, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(21, GPIO.IN)
GPIO.output(19, GPIO.LOW)
m = GPIO.PWM(13,20000)

p = GPIO.PWM(12, 50)
detected = 0
p.start(7.5)
time.sleep(1) # sleep 1 second
p.ChangeDutyCycle(8.5)  # turn towards 0 degree
time.sleep(1) # sleep 1 second
p.ChangeDutyCycle(7.5) # turn towards 180 degree
time.sleep(1) # sleep 1 second
p.stop()

