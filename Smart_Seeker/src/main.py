import time
import numpy as np
import cv2

# Packages
import sys
sys.path.insert(0, '/home/pi/python/Smart_Seeker/src/components/motor')
sys.path.insert(0, '/home/pi/python/Smart_Seeker/src/components/camera')
sys.path.insert(0, '/home/pi/python/Smart_Seeker/src/components/ultrasonic-IR')

# Modules
from init.init import * # (init package.init module)
from Globals.Globals import *

from drive import *
from read_cam import readCam
from find_fingers import findFingers
from find_fist import findFist
from distance import Distance_test
from objects_in_path import objectsInPath


# Driver Code

time.sleep(2)
   
try:
    initialize()

    faces = readCam()
	# ! Here you can implement the face recognizer to check if it is a certain user based on the trainer.yml model built
	
    if Globals.count > 1.0:
        Globals.direction = "right" if Globals.direction == "left" else "left"
        Globals.count = 0.1
    searchDrive(Globals.direction, Globals.count)
    Globals.count = Globals.count + 0.1
    print("searching")
    if len(faces) > 0:
        print("user found")
        brake()
        time.sleep(0.1)
        # wait for okay signal to pursue user
        timeOut = 0
        while not findFingers() and timeOut < 10:
            timeOut = timeOut + 1
            pass
        if timeOut >= 10 : 
            sys.exit("No confirmation of pursuit given, exiting...")
        print("Okay signal given")
        print("pursuing user")
        distance = Distance_test()
        while distance > 15 and not findFist():
            stop = False
            if(findFist() == True):
                print("Stop signal given")
                brake()
                time.sleep(.1)
                stop = True
            while(stop):
                # wait for okay signal to continue
                if(findFigers() == True):
                    print("Okay signal given, continuing pursuit")
                    stop = False     
            if(len(GlobalStacks.speedStack) > 15):
                break
            if(len(GlobalStacks.speedStack) > 0 and Global.failTrigger == False):
                getOnTrack()

            distance = Distance_test()
            objectsInPath(distance)

except KeyboardInterrupt:
    pass
pwm_ENA.stop()
pwm_ENB.stop()
GPIO.cleanup()