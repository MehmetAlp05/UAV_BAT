import numpy as np
import random
class CAV(object):
    def __init__(self):
        self.Speed=random.randint(round(50*(1000/3600)), round(120*(1000/3600)))
        self.EnteringTime=None
        self.PositionVector=None
        self.LeavingTime=None
        self.TaskTimes=None
