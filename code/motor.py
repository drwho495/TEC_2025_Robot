import RPi.GPIO as GPIO
import Encoder
from motorMode import MotorMode
from simple_pid import PID

class Motor:
    def __init__(self, pinA, pinB):
#         GPIO.setmode(GPIO.BCM)
        GPIO.setup(pinA, GPIO.OUT)
        self.pinA_PWM = GPIO.PWM(pinA, 100)
        self.pinA_PWM.start(0)
        
        GPIO.setup(pinB, GPIO.OUT)
        self.pinB_PWM = GPIO.PWM(pinB, 100)
        self.pinB_PWM.start(0)
        
        self.encoder = None
        self.motorMode = MotorMode.SET_POWER
        self.pidController = PID(.005, 0, 0, setpoint=0)
        
        self.motorPower = 0
        self.targetPos = 0
        self.pidOutput = 0
#         self.pinA_PWM.ChangeDutyCycle(50)
        
        print("create motor")
        
    def setEncoder(self, encoder):
        self.encoder = encoder
        
    def getEncoderPos(self):
        return self.encoder.read()
    
    def setMotorMode(self, mode):
        self.motorMode = mode
        
    def setTargetPos(self, pos):
        if self.motorMode == MotorMode.PID:
            self.targetPos = pos
            
    def updatePID(self):
        if self.motorMode == MotorMode.PID:
            self.pidController.setpoint = self.targetPos
            self.pidController.output_limits = (-self.motorPower, self.motorPower)
            motorPos = self.getEncoderPos()
            
            self.pidOutput = self.pidController(motorPos)
            
            if self.pidOutput > 0:
                self.pinA_PWM.ChangeDutyCycle(100 * self.pidOutput)
                self.pinB_PWM.ChangeDutyCycle(0)
            elif self.pidOutput < 0:
                self.pinB_PWM.ChangeDutyCycle(100 * -self.pidOutput)
                self.pinA_PWM.ChangeDutyCycle(0)
            elif self.pidOutput == 0:
                self.pinA_PWM.ChangeDutyCycle(0)
                self.pinB_PWM.ChangeDutyCycle(0)
            
        
    def setPower(self, power):
        self.motorPower = power
        
        out = abs(100 * self.motorPower)
        out = max(0, min(out, 100))
        
        if self.motorMode == MotorMode.SET_POWER:
            if self.motorPower > 0:
                self.pinA_PWM.ChangeDutyCycle(out)
                self.pinB_PWM.ChangeDutyCycle(0)
            elif self.motorPower < 0:
                self.pinB_PWM.ChangeDutyCycle(out)
                self.pinA_PWM.ChangeDutyCycle(0)
            elif self.motorPower == 0:
                self.pinA_PWM.ChangeDutyCycle(0)
                self.pinB_PWM.ChangeDutyCycle(0)
