import cv2
import numpy as np
import math
from enum import Enum

import self as self
from playsound import playsound
from grip import GripPipeline

pipeline = GripPipeline()

vid = cv2.VideoCapture(0)


if (vid.isOpened() == False):
    print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(vid.get(5))
frame_height = int(vid.get(6))

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
#out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'A'), 10, (frame_width, frame_height))

while (True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    vidgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    if ret == True:

        ret, thresh = cv2.threshold(vidgray, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        contour_data = []

        try:
            # Process the Grip Pipeline
            pipeline.process(frame)

            # Populate data from contours
            contour_data = pipeline.find_contours_output

        except (ZeroDivisionError):
            self.logger.logMessage("Divide by 0 exception in GRIP Pipeline")


        cv2.drawContours(frame, contour_data, -1, (0, 255, 0), 3)




        # Display the resulting frame
        cv2.imshow('frame', frame)


        # the 'q' button is set as the
        # quitting button
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#while (True):
#    playsound('beep-01a')

# After the loop release the cap object
vid.release()
#out.release()
# Destroy all the windows
cv2.destroyAllWindows()
