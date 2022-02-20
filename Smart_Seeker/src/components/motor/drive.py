import RPi.GPIO as GPIO
import time

# import package outside directory
import sys
sys.path.insert(0, '/home/pi/python/Smart_Seeker/src/init/')

from init import *

# print(init.IN1) since main uses init module as well, we need to bind our imported module here

#Advance
def run(leftspeed, rightspeed):
    GPIO.output(init.IN1, GPIO.HIGH)
    GPIO.output(init.IN2, GPIO.LOW)
    GPIO.output(init.IN3, GPIO.HIGH)
    GPIO.output(init.IN4, GPIO.LOW)
    init.pwm_ENA.ChangeDutyCycle(leftspeed)
    init.pwm_ENB.ChangeDutyCycle(rightspeed)
    
#back
def back(leftspeed, rightspeed):
    GPIO.output(init.IN1, GPIO.LOW)
    GPIO.output(init.IN2, GPIO.HIGH)
    GPIO.output(init.IN3, GPIO.LOW)
    GPIO.output(init.IN4, GPIO.HIGH)
    init.pwm_ENA.ChangeDutyCycle(leftspeed)
    init.pwm_ENB.ChangeDutyCycle(rightspeed)
	
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
    GPIO.output(init.IN1, GPIO.HIGH)
    GPIO.output(init.IN2, GPIO.LOW)
    GPIO.output(init.IN3, GPIO.LOW)
    GPIO.output(init.IN4, GPIO.LOW)
    init.pwm_ENA.ChangeDutyCycle(leftspeed)
    init.pwm_ENB.ChangeDutyCycle(rightspeed)
	
#turn left in place
def spin_left(leftspeed, rightspeed):
    GPIO.output(init.IN1, GPIO.LOW)
    GPIO.output(init.IN2, GPIO.HIGH)
    GPIO.output(init.IN3, GPIO.HIGH)
    GPIO.output(init.IN4, GPIO.LOW)
    init.pwm_ENA.ChangeDutyCycle(leftspeed)
    init.pwm_ENB.ChangeDutyCycle(rightspeed)

#turn right in place
def spin_right(leftspeed, rightspeed):
    GPIO.output(init.IN1, GPIO.HIGH)
    GPIO.output(init.IN2, GPIO.LOW)
    GPIO.output(init.IN3, GPIO.LOW)
    GPIO.output(init.IN4, GPIO.HIGH)
    init.pwm_ENA.ChangeDutyCycle(leftspeed)
    init.pwm_ENB.ChangeDutyCycle(rightspeed)

#brake
def brake():
   GPIO.output(init.IN1, GPIO.LOW)
   GPIO.output(init.IN2, GPIO.LOW)
   GPIO.output(init.IN3, GPIO.LOW)
   GPIO.output(init.IN4, GPIO.LOW)

#direction driver
def searchDrive(direction, count):
    if direction == "left":
        spin_left(10,10)
    if direction == "right":
        spin_right(10,10)
    if direction == "forward":
        run(10,10)
    time.sleep(count)