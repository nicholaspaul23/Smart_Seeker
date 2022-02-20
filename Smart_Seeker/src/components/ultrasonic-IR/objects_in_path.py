import RPi.GPIO as GPIO
import time

# import package
import sys
sys.path.insert(0, '/home/pi/python/Smart_Seeker/src/init/')
sys.path.insert(0, '/home/pi/python/Smart_Seeker/src/Globals/')
sys.path.insert(0, '/home/pi/python/Smart_Seeker/src/components/motor')

from init import *
from Globals import *
from drive import *

#This functions tests to see if objects are in its path
def objectsInPath(distance):
    #if distance is greater than 50cm/~1.6ft
    LeftIRValue = GPIO.input(init.IRSensorLeft)
    RightIRValue = GPIO.input(init.IRSensorRight)
    #change indicator lights to green for clear
    GPIO.output(init.LED_R, GPIO.LOW)
    GPIO.output(init.LED_G, GPIO.HIGH)
    GPIO.output(init.LED_B, GPIO.LOW)
    
    if distance > 50:
        run(30,30)
        time.sleep(.5)
        GlobalStack.update_timeForward(.5)
        GlobalStack.set_failTrigger(False)
        #check for slanted objects
        #Placed in this block where US sensor won't pick up anything ie >50 but ir sensors pick up a slant outside of US field of view
        if LeftIRValue == False:
            GPIO.output(init.LED_R, GPIO.HIGH)
            GPIO.output(init.LED_G, GPIO.LOW)
            GPIO.output(init.LED_B, GPIO.LOW)
            back(15,15)
            time.sleep(1)
            spin_right(15,15)
            time.sleep(.3)
            GlobalStack.append_speedStack(15)
            GlobalStack.append_durationStack(.3)
            GlobalStack.append_directionStack("right")
            GlobalStack.set_failTrigger(True)
        if RightIRValue == False:
            GPIO.output(init.LED_R, GPIO.HIGH)
            GPIO.output(init.LED_G, GPIO.LOW)
            GPIO.output(init.LED_B, GPIO.LOW)
            back(15,15)
            time.sleep(1)
            spin_left(15,15)
            time.sleep(.3)
            GlobalStack.append_speedStack(15)
            GlobalStack.append_durationStack(.3)
            GlobalStack.append_directionStack("left")
            GlobalStack.set_failTrigger(True)
    elif 30 <= distance <= 50:
        run(15,15)
        time.sleep(.5)
        GlobalStack.update_timeForward(.5)
        GlobalStack.set_failTrigger(False)
        
    #if something is in the way
    elif distance < 30:
        LeftIRValue = GPIO.input(init.IRSensorLeft)
        RightIRValue = GPIO.input(init.IRSensorRight)
            
        if LeftIRValue == True and RightIRValue == True:
            if distance < 20:
                GPIO.output(init.LED_R, GPIO.HIGH)
                GPIO.output(init.LED_G, GPIO.LOW)
                GPIO.output(init.LED_B, GPIO.LOW)
                #if both IR sensors are clear spin slightly to see if one sensor will catch something
                back(10,10)
                time.sleep(.3)
                spin_left(10,10)
                time.sleep(.15)
                GlobalStack.append_speedStack(10)
                GlobalStack.append_durationStack(.15)
                GlobalStack.append_directionStack("left")
                GlobalStack.set_failTrigger(True)
            else:
                #if nothing is caught it will continue to run but slowly
                run(10,10)
                time.sleep(.3)
        elif LeftIRValue == True and RightIRValue == False:
            GPIO.output(init.LED_R, GPIO.HIGH)
            GPIO.output(init.LED_G, GPIO.LOW)
            GPIO.output(init.LED_B, GPIO.LOW)
            back(15,15)
            time.sleep(.7)
            spin_left(15,15) #spin left since there isn't a clear path to the right
            time.sleep(0.3)
            GlobalStack.append_speedStack(15)
            GlobalStack.append_durationStack(.3)
            GlobalStack.append_directionStack("left")
            GlobalStack.set_failTrigger(True)
        elif LeftIRValue == False and RightIRValue == True:
            GPIO.output(init.LED_R, GPIO.HIGH)
            GPIO.output(init.LED_G, GPIO.LOW)
            GPIO.output(init.LED_B, GPIO.LOW)
            back(15,15)
            time.sleep(.7)
            spin_right(15,15)
            time.sleep(0.3)
            GlobalStack.append_speedStack(15)
            GlobalStack.append_durationStack(.3)
            GlobalStack.append_directionStack("right")
            GlobalStack.set_failTrigger(True)
        elif LeftIRValue == False and RightIRValue == False:
            GPIO.output(init.LED_R, GPIO.HIGH)
            GPIO.output(init.LED_G, GPIO.LOW)
            GPIO.output(init.LED_B, GPIO.LOW)
            back(15,15)
            time.sleep(.7)
            spin_left(15,15)
            time.sleep(0.3)
            GlobalStack.append_speedStack(15)
            GlobalStack.append_durationStack(.3)
            GlobalStack.append_directionStack("left")
            GlobalStack.set_failTrigger(True)
            

#this function gets the robot back on its orignal path after obstacle avoidance
#this function utilizes run times, turn speeds and spin angles to process robot orientation
#using a vector like model we can reposition the robot by reversing the steps
#i.e. using the reverse of the spin angle and run times to calculate length of resultant to get back on track
def getOnTrack():
    print ("Correcting Path...")
    #print direction stack
    for x in directionStack:
        print(x)
    #wait
    while(len(speedStack) > 1):
        moveCount = len(speedStack) - 1
        
        if(directionStack[moveCount] == "right"):
            spin_left(speedStack[moveCount],speedStack[moveCount])
            print("Correcting left")
        else:
            spin_right(speedStack[moveCount],speedStack[moveCount])
            print("Correcting right")
                
        time.sleep(durationStack[moveCount] + .35)
        
        GlobalStack.pop_speedStack()
        GlobalStack.pop_durationStack()
        GlobalStack.pop_directionStack()
        
    #final repositioning cleanup
    if(directionStack[0] == "right"):
        spin_left(speedStack[0],speedStack[0])
        time.sleep(durationStack[0] + .35)
        print("Correcting left")
        GlobalStack.pop_speedStack()
        GlobalStack.pop_durationStack()
        GlobalStack.pop_directionStack()
        #check again for a clear path to correct
        #27 bc sometimes the US snesor gets stuck on 30 bc of calibration issues
        if(Distance_test() < 27):
            #adjust buffer angle 
            spin_right(15,15)
            time.sleep(.05)
            return
        run(22,22)
        time.sleep(GlobalStack.timeForward)
        spin_right(15,15)
        time.sleep(.1)
    else:
        spin_right(speedStack[0],speedStack[0])
        time.sleep(durationStack[0] + .35)
        print("Correcting right")
        GlobalStack.pop_speedStack()
        GlobalStack.pop_durationStack()
        GlobalStack.pop_directionStack()
        if(Distance_test() < 27):
            spin_left(15,15)
            time.sleep(.05)
            return
        run(22,22)
        time.sleep(GlobalStack.timeForward)
        spin_left(15,15)
        time.sleep(.1)
    #reset timeFowrard   
    GlobalStack.reset_timeForward()