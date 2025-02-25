import RPi.GPIO as GPIO
import time
from parameters import Parameters
from states import States
from timer import Timer
from evdev import InputDevice, categorize, ecodes
from gamepad import Gamepad
from motor import Motor

#creates object 'gamepad1' to store the data
#you can call it whatever you like
gamepad1 = Gamepad('/dev/input/event1')

robotRunning = True
led = None
params = Parameters()
state = None
stateStart = False
timer = Timer()
hertz = 0
driveMotorLeft = None

def setState(_state):
    global state
    global stateStart
    
    if(type(_state) == States):
        state = _state
        stateStart = True

def setup():
    global robotRunning
    global params
    global led
    global state
    global hertz
    global gamepad1
    global driveMotorLeft
        
#     driveMotorLeft.setPower(.5)
        
    setState(States.IDLE)
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.OUT)
    led = GPIO.PWM(16, 10000)
    robotRunning = True
    hertz = 0
    
    driveMotorLeft = Motor(6, 5)
    
    gamepad1.startLoop()

    led.start(params.ledPower)

def clearScreen():
    enterLines = 35
    
    for i in range(enterLines):
        print("\n")

def stop():
    led.stop()
    GPIO.cleanup()

def startLoop():
    global robotRunning
    global led
    global params
    global state
    global stateStart
    global timer
    global hertz
    global gamepad1
    global hotkeys
    global driveMotorLeft
    
    robotRunning = True
    
    while robotRunning:
#         print(gamepad1.loopRunning())
                
        if timer.time() > 1000.0:
            print(hertz)
            hertz = 0
            timer.reset()
        else:
            hertz += 1
        
        try:
            ## State based code ##
            if state == States.IDLE:
                if stateStart:
                    clearScreen()
                    print("Current State: " + str(state))
                    led.ChangeDutyCycle(params.ledPower)
                    
                #print("a: ", gamepad1.a)
                #print("lsy: ", gamepad1.left_stick_y)
                #print("lsx: ", gamepad1.left_stick_x)
                
                driveMotorLeft.setPower(gamepad1.left_stick_y)
                
                if gamepad1.a == True:
                    led.ChangeDutyCycle(0)
                else:
                    led.ChangeDutyCycle(params.ledPower)
            if state == States.MAIN:
                if stateStart:
                    clearScreen()
                    timer.reset()
                    print("Current State: " + str(state))
                
                if timer.time() > 0.0 and timer.time() < 500.0:
                    led.ChangeDutyCycle(0)
                else:
                    led.ChangeDutyCycle(params.ledPower)
                    
            ## Global code ##
            stateStart = False
        except KeyboardInterrupt:
            robotRunning = False
    
    stop()
    
if __name__ == "__main__":
    setup()
    startLoop()
    