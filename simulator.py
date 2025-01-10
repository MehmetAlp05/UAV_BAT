import numpy as np
from classes.cav import CAV
import math
from parameters import Parameters

# TASK GENERATION
m=1
tau=400 #simulation time
lam=1/tau 
task_arrival=np.random.poisson(lam,tau)
print(task_arrival.shape)
print(np.sum(task_arrival))

def TaskGenerator(runtime,num_event):
    task_arrival=np.random.poisson(num_event/runtime,runtime)
    return task_arrival

### CAVS
car_rate=.5
sim_runtime=tau
car_arrivals=np.random.poisson(car_rate,sim_runtime)
print("car_arrivals\n",car_arrivals)
print("car_arrivals.shape\n",car_arrivals.shape)
print("np.sum(car_arrivals)\n",np.sum(car_arrivals))

#monte carlo test
monte=[]
for index in range(1000):
    car_arrivals=np.random.poisson(car_rate,sim_runtime)
    monte.append(np.sum(car_arrivals))
monte=np.array(monte)
print("monte carlo test",np.average(monte))

#example object generation
cav=CAV()
cav.EnteringTime=30
cav.LeavingTime=tau
cav.PositionVector=[1,2,3,4,5]
cav.TaskTimes=[10,20,30,40]


car_arrivals=np.random.poisson(car_rate,sim_runtime)#car_arrival generator
cav_number=np.sum(car_arrivals)#total car number by car arrival
indices_of_arrivals=np.where(car_arrivals==1)[0]#for what time index cars enters the road
CAVs=np.array([CAV() for index,arrival in enumerate(indices_of_arrivals)])#car object generation
print("indices_of_arrivals\n",indices_of_arrivals)
#CAV object value assignments
for index,arrival in enumerate(indices_of_arrivals):
    #entering time
    CAVs[index].EnteringTime=arrival
    #calculation of the leaving time corresponding to road parameters
    CAVs[index].LeavingTime=int(arrival+(Parameters.RoadLength/CAVs[index].Speed))
    #position vector of the car
    CAVs[index].PositionVector=np.zeros(Parameters.RoadLength)
    for index_ in range(Parameters.RoadLength):
        if index_ > arrival and index_<CAVs[index].LeavingTime:
            CAVs[index].PositionVector[index_]=CAVs[index].PositionVector[index_-1]+CAVs[index].Speed
    #task generation for corresponding cars
    Tasks=TaskGenerator((CAVs[index].LeavingTime-CAVs[index].EnteringTime),1)
    print("index and task",index,Tasks)
    print("nerede",np.where(Tasks > 0)[0]+arrival)
    CAVs[index].TaskTimes = np.where(Tasks > 0)[0] + arrival if np.all(np.where(Tasks > 0)[0] + arrival < tau) else []
    print("CAV #",index)
    print("Entering Time",CAVs[index].EnteringTime)
    print("Leaving Time",CAVs[index].LeavingTime)
    print("Task Times",CAVs[index].TaskTimes)
    print("Position Vector",CAVs[index].PositionVector)

np.save("./data/CAVs.npy",CAVs)
allTask=np.zeros(Parameters.T)
for index in range(len(CAVs)):
    print("cav task time",index,CAVs[index].TaskTimes)
    for index_,element_ in enumerate(CAVs[index].TaskTimes):
        allTask[element_]=index
np.save("./data/allTask.npy",allTask)
leavingTimes=np.zeros(len(CAVs))
for index in range(len(CAVs)):
    print("cav leaving time",index,CAVs[index].LeavingTime)
    leavingTimes[index]=CAVs[index].LeavingTime
np.save("./data/leavingTimes.npy",leavingTimes)
"""
def Gain(CAVPos,UAVPos):
    gain=10**(Parameters.G0/10)/(math.sqrt(Parameters.H**2+(CAVPos-UAVPos)**2))**2;
    return gain
gain=Gain(220,500)

def UplinkRate(CAVPos,UAVPos):
    gain=Gain(CAVPos,UAVPos)
    rate=math.log2(1+(gain*((10**(Parameters.Pm/10))/(10**(Parameters.N0/10)*Parameters.B))))*Parameters.B;
    return rate
u_rate=UplinkRate(1000,0)
print("uplink rate",u_rate)
"""


