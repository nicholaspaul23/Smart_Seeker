import RPi.GPIO as GPIO
import time

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

#Set PWM
GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
pwm_ENA = GPIO.PWM(ENA, 2000)
pwm_ENB = GPIO.PWM(ENB, 2000)



#initialize inputs and outputs
def initialize():
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
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
    #Set the PWM pin and frequency to 2000hz
    pwm_ENA.start(0)
    pwm_ENB.start(0)
    #initialize servo
    GPIO.setup(ServoPin, GPIO.OUT)
    pwm_servo = GPIO.PWM(ServoPin, 50)
    pwm_servo.start(0)
    
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