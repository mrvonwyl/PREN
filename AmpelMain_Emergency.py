import cv2
import time
from TrafficLightDetection import *
from Serial import Serial

class MainAmpelerkennung:
    def __init__(self):
        print('init Ampelerkennung')

    def detect_light(self):
        print('Start Capture')

        # initialize serial connection
        ser = Serial()

        # start the video capture
        camera = cv2.VideoCapture(1)

        # Load an image
        #frame = cv2.imread('images/ampel_red.png')
        #frame = cv2.imread('images/ampel_green.png')
        #frame = cv2.imread('images/color_gradient.png')

        # Load a video
        #camera = cv2.VideoCapture('videos/AmpelTest.mp4')

        # initialize variables for traffic light detection
        # loop: initial state TRUE to run the loop and FALSE to stop the loop
        # traffic_light: initial state red = FALSE and green = TRUE
        # emergency_counter: a counter to prevent the pink panzer form never starting
        # even if no signal from the traffic light can be detected
        loop = True
        traffic_light = 's'
        emergency_counter = 0

        # looping while video capture is active
        if (camera.isOpened()):
            while (loop):

                # if the counter reaches 200, the go siganl will be given
                # regardless of the traffic light
                if (emergency_counter < 200):

                    print (traffic_light)

                    # grab the current frame
                    _, frame = camera.read()

                    # prepare the frame for color detection
                    prepped_frame = frame_prep(frame)

                    # set the color for color detection and create
                    # a mask by checking for red and green traffic lights
                    mask = color_detection(prepped_frame, 'green')

                    # find contours in the mask and initialize the current
                    # (x, y) center of the ball
                    contour = contour_detection(mask)

                    # give the go-signal when a matching contour was found
                    traffic_light = go_time(contour)

                    # stop the loop if it is go time
                    if (traffic_light == 'g'):
                        print (traffic_light)
                        print ('Green Light detected')
                        loop = False

                    # increase the emergency counter
                    emergency_counter += 1

                    cv2.imshow('frame', frame)
                    cv2.imshow('prepped_frame', prepped_frame)
                    cv2.imshow('mask', mask)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                else:
                    # stop the loop if the emergency counter reaches 100
                    # and set the traffic light variable accordingly
                    traffic_light = 'g'
                    loop = False
                    print (traffic_light)
                    print ('Emergency Loop exeeded')

                    cv2.imshow('frame', frame)
                    cv2.imshow('prepped_frame', prepped_frame)
                    cv2.imshow('mask', mask)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        else:
            print('No Video Capture detected')

        print ('Go Time')
        camera.release()
        cv2.destroyAllWindows()
        ser.sendText(traffic_light)

