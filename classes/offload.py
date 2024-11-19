import numpy as np
import math
class Offload:
    def __init__(self):
        self.alpha=12*10**6
        self.cycle_per_bit=1000
        self.cycle_per_second=10**9
        self.G0=-50
        self.height=80
        self.Pm=35
        self.N0=-130
        self.B=20*10**6
    def process_delay(self):
        delay=self.alpha*self.cycle_per_bit/self.cycle_per_second
        return delay
    def gain(self,CAV,UAV):
        self.gain=10**(self.G0/10)/(math.sqrt(self.height**2+(CAV.Position-UAV.Position)**2))**2
        return self.gain
    def uplink_rate(self,gain):
        self.rate=math.log2(1+(gain*((10**(self.Pm/10))/(10**(self.N0/10)*self.B))))*self.B
        return self.rate
    

