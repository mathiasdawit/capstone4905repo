#Import Necessary Packages
import cv2
import time  
import numpy as np
import math
from enum import Enum
import self as self
from grip import GripPipeline
import pygame
from picamera.array import PiRGBArray
from picamera import PiCamera
import obd

# Pipeline Constructor
pipeline = GripPipeline()
pygame.mixer.init()
pygame.mixer.music.load('beep-01b.mp3')

# Constructing Camera Object
camera = PiCamera()
camera.resolution = (640,480)
#camera.resolution = (1920,1080)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))
time.sleep(0.1)

# Creating OBD connection
ports = obd.scan_serial()
connection = obd.OBD(ports[0])
cmd = obd.commands.SPEED


# Loop reads from camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	
    frame = rawCapture.array 
    vidgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #
    contours, hierarchy = cv2.findContours(vidgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    try:
        # Process the Grip Pipeline
        pipeline.process(frame)
        # Populate data from contours
        contour_data = pipeline.find_contours_output
    except (ZeroDivisionError):
        self.logger.logMessage("Divide by 0 exception in GRIP Pipeline")
            
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        if len(approx) > 25:
            cv2.drawContours(frame, contour_data, -1, (0, 255, 0), 3)
    
    # show the frame
    cv2.imshow("Frame", frame)
    
    response = connection.query(cmd)
    speed = response.value.to("mph").magnitude
    print(speed)
    
    
    # play noise if red light detected AND car speed > 0
    if ( len(contour_data) > 0 and speed > 0.0 ):   
        print("beep")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            pygame.time.delay(200)
            continue
    
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    
    # if the `q` key was pressed, break from the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    
cv2.destroyAllWindows() 

