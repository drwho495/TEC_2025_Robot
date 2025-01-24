import time

class Timer:
    def reset(self):
        self.start = time.time()
    
    def __init__(self):
        self.reset()
        
    def time(self):
        return (time.time() - self.start)*1000
    