import RPi.GPIO as GPIO
import time
from parameters import Parameters
from states import States
from motorMode import MotorMode
from timer import Timer
from evdev import InputDevice, categorize, ecodes
from gamepad import Gamepad
from motor import Motor
import Encoder
import os

#creates object 'gamepad1' to store the data
#you can call it whatever you like

gamepad1 = Gamepad('/dev/input/event1')

robotRunning = True
led = None
params = Parameters()
state = None
stateStart = False
timer = Timer()
optionsTimer = Timer()
shareTimer = Timer()
hertz = 0
driveMotorLeft = None
driveMotorRight = None

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
    global driveMotorRight
    global slidesMotor
        
#     driveMotorLeft.setPower(.5)
        
    setState(States.IDLE)
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.OUT)
    led = GPIO.PWM(16, 10000)
    robotRunning = True
    hertz = 0
    
    driveMotorLeft = Motor(6, 5)
    driveMotorRight = Motor(23, 24)
    slidesMotor = Motor(13, 19)
    slidesMotor.setEncoder(Encoder.Encoder(22, 27))
    slidesMotor.setMotorMode(MotorMode.PID)
    
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
    global optionsTimer
    global shareTimer
    global hertz
    global gamepad1
    global hotkeys
    global driveMotorLeft
    global driveMotorRight
    global slidesMotor
    
    robotRunning = True
    optionsCooldown = False
    shareCooldown = False
    
    while robotRunning:
#         print(gamepad1.loopRunning())
        try:
            if not gamepad1.options:
                optionsCooldown = False
                
            if not gamepad1.share:
                shareCooldown = False
            
            if timer.time() > 1000.0:
                gamepad1.update()
                
                if not gamepad1.connected:
                    print(gamepad1.connected)
                
                print(hertz)
                hertz = 0
                timer.reset()
            else:
                hertz += 1
                        ## State based code ##
            if state == States.IDLE:
                if stateStart:
                    clearScreen()
                    print("Current State: " + str(state))
                    led.ChangeDutyCycle(params.ledPower)
                    
#                 print("lsy: ", gamepad1.left_stick_y)
#                 print("lsx: ", gamepad1.left_stick_x)

                print("slidesMotor Encoder Pos: " + str(slidesMotor.getEncoderPos()))
                print("pid output: " + str(slidesMotor.pidOutput))
                
                slidesMotor.setTargetPos(3000)
                slidesMotor.setPower(1)
                
                driveMotorLeft.setPower(gamepad1.left_stick_y)
                
                if gamepad1.options:
                    if not optionsCooldown:
                        optionsTimer.reset()
                    
                    if optionsTimer.time() >= 1000.0:
                        setState(States.MAIN)
                        continue
                    
                    optionsCooldown = True
                    
                if gamepad1.a:
                    led.ChangeDutyCycle(0)
                else:
                    led.ChangeDutyCycle(params.ledPower)
            if state == States.MAIN:
                if stateStart:
                    clearScreen()
                    timer.reset()
                    print("Current State: " + str(state))
                    
                drivePower = gamepad1.left_stick_y;
                rotatePower = gamepad1.right_stick_x;
                
                if abs(drivePower) < .1:
                    drivePower = 0
                    
                if abs(rotatePower) < .1:
                    rotatePower = 0

                driveMotorLeft.setPower(drivePower + rotatePower);
                driveMotorRight.setPower(drivePower - rotatePower);
                    
                if gamepad1.share:
                    if not shareCooldown:
                        shareTimer.reset()
                    
                    if shareTimer.time() >= 1000.0:
                        setState(States.IDLE)
                        continue
                    
                    shareCooldown = True
                
                if timer.time() > 0.0 and timer.time() < 500.0:
                    led.ChangeDutyCycle(0)
                else:
                    led.ChangeDutyCycle(params.ledPower)
                    
            ## Global code ##
            stateStart = False
            slidesMotor.updatePID()
        except KeyboardInterrupt:
            robotRunning = False
            break
    
    stop()
    
if __name__ == "__main__":
    setup()
    startLoop()
    