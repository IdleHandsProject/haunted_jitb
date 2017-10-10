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
#p.start(7.5)
#time.sleep(1) # sleep 1 second
#p.ChangeDutyCycle(8.5)  # turn towards 0 degree
#time.sleep(1) # sleep 1 second
#p.ChangeDutyCycle(7.5) # turn towards 180 degree
#time.sleep(1) # sleep 1 second
#p.stop()
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 30
camera.color_effects = (128,128)
camera.vflip = True 
rawCapture = PiRGBArray(camera, size=(320, 240))
 
# Create the haar cascade.  This should be a trained file for face (but can be anything really)

faceCascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
bodyCascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_upperbody.xml')
 
# allow the camera to warmup
time.sleep(0.1)
m.start(0)
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image
    image = frame.array
 
    # This is required when you do loops, otherwise the frame will be full on the next iteration
    frame.truncate(0)
 
    # Convert it to grayscale for the faceCascade
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = image
    # Find all the faces using the Cascade Classifier
#    body = bodyCascade.detectMultiScale(
#        gray,
#        scaleFactor=1.2,
#        minNeighbors=5,
#        minSize=(30, 30),
#        flags=cv2.CASCADE_SCALE_IMAGE
#    )

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    if (detected == 0):
        if (len(faces)>0):
            detected = 1
	    print "Human Detected"

    if (detected == 1):
        if (GPIO.input(21) == True):
	    print "end detected"
	    m.ChangeDutyCycle(10)
	    time.sleep(0.5)
	    m.ChangeDutyCycle(0)
            time.sleep(3)
            m.ChangeDutyCycle(50)
	    p.start(7.5)
	    time.sleep(0.1) # sleep 1 second
	    p.ChangeDutyCycle(8.5)  # turn towards 0 degree
	    time.sleep(1) # sleep 1 second
	    p.ChangeDutyCycle(7.5) # turn towards 180 degree
	    time.sleep(1) # sleep 1 second
	    p.stop()
            m.stop()
	    while(True):
		pass

        if (len(faces)>0):
            m.ChangeDutyCycle(0)
        else:
            m.ChangeDutyCycle(10)
        for (x, y, w, h) in faces:
            print "Face at %d, %d" % (x + (w / 2), y + (h / 2))
