import RPi.GPIO as GPIO
import time

# import package
import sys
sys.path.insert(0, '/home/pi/python/Smart_Seeker/src/init/')

from init import *

# get distance with ultrasonic module
def Distance():
    GPIO.output(init.TrigPin,GPIO.LOW)
    time.sleep(0.000002)
    GPIO.output(init.TrigPin,GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(init.TrigPin,GPIO.LOW)

    t3 = time.time()

    while not GPIO.input(init.EchoPin):
        t4 = time.time()
        if (t4 - t3) > 0.03 :
            return -1


    t1 = time.time()
    while GPIO.input(init.EchoPin):
        t5 = time.time()
        if(t5 - t1) > 0.03 :
            return -1

    t2 = time.time()
    time.sleep(0.01)
    return ((t2 - t1)* 340 / 2) * 100

# get averages of distance based on ultrasonic execution
def Distance_test():
    num = 0
    ultrasonic = []
    while num < 5:
            distance = Distance()
            while int(distance) == -1 :
                distance = Distance()
            while (int(distance) >= 500 or int(distance) == 0) :
                distance = Distance()
            ultrasonic.append(distance)
            num = num + 1
            time.sleep(0.01)
    
    distance = (ultrasonic[1] + ultrasonic[2] + ultrasonic[3])/3
    print("distance is %f"%(distance) ) 
    return distance