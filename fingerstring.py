import cv2
import detectFingers as dtctFing
import abletonInteraction as ableInt
import screenDrawing as scrDraw
import numpy as np
from pythonosc.udp_client import SimpleUDPClient

ip = "127.0.0.1" #localhost
toAbleton = 11000
fromAbleton = 11001
udpClient = SimpleUDPClient(ip, toAbleton)

# Open the default camera
cam = cv2.VideoCapture(0)

# Get the default frame width and height
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
quarter_width = int(frame_width / 4)



while True:

    left_finger_data = None
    right_finger_data = None

    ret, frame = cam.read()

    frame = cv2.flip(frame, 1)

    fingerTipSets = dtctFing.detectFingers(frame)

    left_finger_data, right_finger_data = scrDraw.processHandData(fingerTipSets, frame_width, frame_height, frame)

    # send the pinch magnitudes to Ableton
    ableInt.take_finger_data(left_finger_data, right_finger_data, udpClient)

    # Display the captured frame
    cv2.imshow('Camera', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and writer objects
cam.release()
cv2.destroyAllWindows()