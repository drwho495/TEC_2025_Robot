import RPi.GPIO as GPIO
import time
from parameters import Parameters
from states import States
from timer import Timer

robotRunning = True
led = None
params = Parameters()
state = None
stateStart = False
timer = Timer()

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
    
    setState(States.IDLE)
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.OUT)
    led = GPIO.PWM(16, 150)
    robotRunning = True

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
    
    robotRunning = True
    
    while robotRunning:
        try:
            ## State based code ##
            if state == States.IDLE:
                if stateStart:
                    clearScreen()
                    print("Current State: " + str(state))
                
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
                    
                if timer.time() > 1000.0:
                    timer.reset()
                    
            ## Global code ##
            stateStart = False
        except KeyboardInterrupt:
            robotRunning = False
    
    stop()
    
if __name__ == "__main__":
    setup()
    startLoop()
    