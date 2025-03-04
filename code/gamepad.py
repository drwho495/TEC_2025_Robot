from evdev import InputDevice, categorize, ecodes
import threading
import time
import os

class Gamepad:
    def _updateConnected(self):
        if self.useDevice:
            self.connected = os.path.exists(self.gamepadLoc)
    
    def _main(self):
        self.threadRunning = True
        
        while True:
            try:
                if self.connected:
                    for ev in self.gamepad.read_loop():
                        if ev.code == 304: # A Button
                            if ev.value == 1:
                                self.a = True
                            else:
                                self.a = False
                        elif ev.code == 1:
                            self.left_stick_y = (ev.value-(127.5))/-127.5
                        elif ev.code == 0:
                            self.left_stick_x = (ev.value-(127.5))/-127.5
                        elif ev.code == 2:
                            self.right_stick_x = (ev.value-(127.5))/-127.5
                        elif ev.code == 5:
                            self.right_stick_y = (ev.value-(127.5))/-127.5
                #                 print((ev.value-(127.5))/-127.5)
                        elif ev.code == 315: # Options
                            if ev.value == 1:
                                self.options = True
                            else:
                                self.options = False
                        elif ev.code == 314: # Options
                            if ev.value == 1:
                                self.share = True
                            else:
                                self.share = False
                        else:
#                             print(ev)
                            pass
                            
                #             time.sleep(1/1000)
            except:
                 pass
            
            time.sleep(1)
        self.threadRunning = False
            
    def loopRunning(self):
        return self.threadRunning
    
    def startLoop(self):
        if self.useDevice:
            self.thread.start()
        
    def update(self):
        self._updateConnected()
        
        if self.connected:
            self.connect()
            
#             if not self.threadRunning:
#                 self.startLoop()
                
            
    def connect(self):
        if(self.useDevice):
            if self.connected:
                self.gamepad = InputDevice(self.gamepadLoc)
            else:
                self.gamepad = None
                pass
    
    def __init__(self, gamepadLoc):
        if gamepadLoc != False:
            self.gamepadLoc = gamepadLoc
            self.useDevice = True
            self._updateConnected()
            self.connect()
            self.threadRunning = False
        else:
            self.useDevice = False
        
        self.thread = threading.Thread(target=self._main, args=())
        
        self.a = False
        self.b = False
        self.x = False
        self.y = False
    
        self.right_stick_x = 0
        self.right_stick_y = 0
        
        self.left_stick_x = 0
        self.left_stick_y = 0
        
        self.options = False
        self.share = False
        
        
if __name__ == "__main__":
#     gamepad1 = InputDevice('/dev/input/event1')
#     
#     print(gamepad1)
#     
#     gp1Loop = gamepad1.read_loop()
#         
#     for event in gamepad1.read_loop():
#         print(categorize(event))
    gp = Gamepad("/dev/input/event1")
    
    gp.startLoop()
    while True:
        print(os.path.exists(gp.gamepadLoc))
        time.sleep(1)
        continue
#         print(gp.a)