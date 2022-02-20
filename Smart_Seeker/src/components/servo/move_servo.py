from init import *
import time

def move_servo(angle):
    GPIO.output(ServoPin, True)
    pwm_servo.ChangeDutyCycle(angle / 18 +2) # 10 deg from origin on right
    time.sleep(1)
    GPIO.output(ServoPin, False)
    pwm_servo.ChangeDutyCycle(0)