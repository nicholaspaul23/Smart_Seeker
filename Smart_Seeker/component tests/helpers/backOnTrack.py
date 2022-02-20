import RPi.GPIO as GPIO
import time

'''
    Notes
-Objects blocking left causes robot to turn left instead of right -> IR sensor recalibrated [GOOD]

- During correction it should still check for objects in path
    (this will also fix the issue with error correction for slanted objects)
    *Fix in another file
    *Calling the function recursively screws up the stack variables, maybe just add a distance check and
    a return to driver loop. (watch out for timeFoward = 0 statement)

- 1. The run speed for the correction algorithim is an average of the speeds encountered
  by distances [30,50] and >50
  2. The spin times are adjusted by a final factor +.35 s
  
  * The more corrections -> the higher chance of error getting back on original path

'''

#define pins
#Motor
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13
#start button
key = 8
#ultrasonic module
EchoPin = 0
TrigPin = 1
#infrared module
IRSensorLeft = 12
IRSensorRight = 17
#servo for Ultrasonic Sensor
ServoPin = 23
#Definition of RGB module pins
LED_R = 22
LED_G = 27
LED_B = 24

#set GPIO port mode to BCM
GPIO.setmode(GPIO.BCM)

#escape warnings
GPIO.setwarnings(False)

#set global failTrigger variable
#for avoiding objects protocols
failTrigger = False

#set global variable for how far robot has progressed forward since last failTrigger
timeForward = 0.0
    
#set lists for recording moves
speedStack = []
durationStack = []
directionStack = []


#initialize inputs and outputs
def init():
    global pwm_ENA
    global pwm_ENB
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(key,GPIO.IN)
    GPIO.setup(EchoPin,GPIO.IN)
    GPIO.setup(TrigPin,GPIO.OUT)
    GPIO.setup(IRSensorLeft, GPIO.IN)
    GPIO.setup(IRSensorRight, GPIO.IN)
    GPIO.setup(LED_R, GPIO.OUT)
    GPIO.setup(LED_G, GPIO.OUT)
    GPIO.setup(LED_B, GPIO.OUT)
    #Turn indicator light green
    GPIO.output(LED_R, GPIO.LOW)
    GPIO.output(LED_G, GPIO.HIGH)
    GPIO.output(LED_B, GPIO.LOW)
    #Set the PWM pin and frequency is 2000hz
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)
    #initialize servo
    GPIO.setup(ServoPin, GPIO.OUT)
    pwm_servo = GPIO.PWM(ServoPin, 50)
    pwm_servo.start(0)
	
#Advance
def run(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

#back
def back(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)
	
#turn left
def left(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

#turn right
def right(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)
	
#turn left in place
def spin_left(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

#turn right in place
def spin_right(leftspeed, rightspeed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(leftspeed)
    pwm_ENB.ChangeDutyCycle(rightspeed)

#brake
def brake():
   GPIO.output(IN1, GPIO.LOW)
   GPIO.output(IN2, GPIO.LOW)
   GPIO.output(IN3, GPIO.LOW)
   GPIO.output(IN4, GPIO.LOW)

#detect start button press
def key_scan():
    while GPIO.input(key):
        pass
    while not GPIO.input(key):
        time.sleep(0.01)
        if not GPIO.input(key):
            time.sleep(0.01)
        while not GPIO.input(key):
            pass

#get distance with ultrasonic module
def Distance():
    GPIO.output(TrigPin,GPIO.LOW)
    time.sleep(0.000002)
    GPIO.output(TrigPin,GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TrigPin,GPIO.LOW)

    t3 = time.time()

    while not GPIO.input(EchoPin):
        t4 = time.time()
        if (t4 - t3) > 0.03 :
            return -1


    t1 = time.time()
    while GPIO.input(EchoPin):
        t5 = time.time()
        if(t5 - t1) > 0.03 :
            return -1

    t2 = time.time()
    time.sleep(0.01)
    return ((t2 - t1)* 340 / 2) * 100

#get averages of distance based on ultrasonic execution
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

#The US servo rotates to the specified angle
def move_servo(pos):
    for i in range(18):
        pwm_servo.ChangeDutyCycle(2.5 + 10 * pos/180)
        
#This functions tests to see if objects are in its path
def objectsInPath(distance):
    #if distance is greater than 50cm/~1.6ft
    LeftIRValue = GPIO.input(IRSensorLeft)
    RightIRValue = GPIO.input(IRSensorRight)
    #change indicator lights to green for clear
    GPIO.output(LED_R, GPIO.LOW)
    GPIO.output(LED_G, GPIO.HIGH)
    GPIO.output(LED_B, GPIO.LOW)
    global failTrigger
    global timeForward #sometimes you have to declare variables you make assigments to locally in a function global
    #since python treats global variables locally if they are manipulated/assigned in a function body
    #we use global to make it like a static variable
    
    if distance > 50:
        run(30,30)
        time.sleep(.5)
        timeForward += .5
        failTrigger = False
        #check for slanted objects
        #Placed in this block where US sensor won't pick up anything ie >50 but ir sensors pick up a slant outside of US field of view
        if LeftIRValue == False:
            GPIO.output(LED_R, GPIO.HIGH)
            GPIO.output(LED_G, GPIO.LOW)
            GPIO.output(LED_B, GPIO.LOW)
            back(15,15)
            time.sleep(1)
            spin_right(15,15)
            time.sleep(.3)
            speedStack.append(15)
            durationStack.append(.3)
            directionStack.append("right")
            failTrigger = True
        if RightIRValue == False:
            GPIO.output(LED_R, GPIO.HIGH)
            GPIO.output(LED_G, GPIO.LOW)
            GPIO.output(LED_B, GPIO.LOW)
            back(15,15)
            time.sleep(1)
            spin_left(15,15)
            time.sleep(.3)
            speedStack.append(15)
            durationStack.append(.3)
            directionStack.append("left")
            failTrigger = True
    elif 30 <= distance <= 50:
        run(15,15)
        time.sleep(.5)
        timeForward += .5
        failTrigger = False
    #if something is in the way
    elif distance < 30:
        LeftIRValue = GPIO.input(IRSensorLeft)
        RightIRValue = GPIO.input(IRSensorRight)
            
        if LeftIRValue == True and RightIRValue == True:
            if distance < 20:
                GPIO.output(LED_R, GPIO.HIGH)
                GPIO.output(LED_G, GPIO.LOW)
                GPIO.output(LED_B, GPIO.LOW)
                #if both IR sensors are clear spin slightly to see if one sensor will catch something
                back(10,10)
                time.sleep(.3)
                spin_left(10,10)
                time.sleep(.15)
                speedStack.append(10)
                durationStack.append(.15)
                directionStack.append("left")
                failTrigger = True
            else:
                #if nothing is caught it will continue to run but slowly
                run(10,10)
                time.sleep(.3)
                #timeForward = timeForward + .3
        elif LeftIRValue == True and RightIRValue == False:
            GPIO.output(LED_R, GPIO.HIGH)
            GPIO.output(LED_G, GPIO.LOW)
            GPIO.output(LED_B, GPIO.LOW)
            back(15,15)
            time.sleep(.7)
            spin_left(15,15) #spin left since there isn't a clear path to the right
            time.sleep(0.3)
            speedStack.append(15)
            durationStack.append(.3)
            directionStack.append("left")
            failTrigger = True
        elif LeftIRValue == False and RightIRValue == True:
            GPIO.output(LED_R, GPIO.HIGH)
            GPIO.output(LED_G, GPIO.LOW)
            GPIO.output(LED_B, GPIO.LOW)
            back(15,15)
            time.sleep(.7)
            spin_right(15,15)
            time.sleep(0.3)
            speedStack.append(15)
            durationStack.append(.3)
            directionStack.append("right")
            failTrigger = True
        elif LeftIRValue == False and RightIRValue == False:
            GPIO.output(LED_R, GPIO.HIGH)
            GPIO.output(LED_G, GPIO.LOW)
            GPIO.output(LED_B, GPIO.LOW)
            back(15,15)
            time.sleep(.7)
            spin_left(15,15)
            time.sleep(0.3)
            speedStack.append(15)
            durationStack.append(.3)
            directionStack.append("left")
            failTrigger = True

#this function gets the robot back on its orignal path after obstacle avoidance
#this function utilizes run times, turn seeds and spin angles to process robot orientation
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
    
        speedStack.pop()
        durationStack.pop()
        directionStack.pop()
        
    #final repositioning cleanup
    if(directionStack[0] == "right"):
        spin_left(speedStack[0],speedStack[0])
        time.sleep(durationStack[0] + .35)
        print("Correcting left")
        speedStack.pop()
        durationStack.pop()
        directionStack.pop()
        run(22,22)
        time.sleep(timeForward)
        spin_right(15,15)
        time.sleep(.4)
    else:
        spin_right(speedStack[0],speedStack[0])
        time.sleep(durationStack[0] + .35)
        print("Correcting right")
        speedStack.pop()
        durationStack.pop()
        directionStack.pop()
        run(22,22)
        time.sleep(timeForward)
        spin_left(15,15)
        time.sleep(.4)
            

#DRIVER CODE
time.sleep(2)

try:
    init()
    key_scan()
    print ("success")
        
    while True:
        if(len(speedStack) > 15):
           break
        if(len(speedStack) > 0 and failTrigger == False):
            #check for failTrigger false meaning we have successfully avoided and cleared the object run(30,30)
            getOnTrack()
            timeForward = 0
        distance = Distance_test()
        objectsInPath(distance)
except KeyboardInterrupt:
    pass
pwm_ENA.stop()
pwm_ENB.stop()
GPIO.cleanup()