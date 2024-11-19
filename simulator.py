import numpy as np
from classes.cav import CAV
from classes.offload import Offload
import math
# Parameters
alpha=12*10^6;#bits
T=400;#seconds
sigma=1;#Time slot (in seconds)
C=1000;#cycle per bit
f=2*10^9;#ycle per second
G0=-50;#dB
H=80;#meters
N0=-130;#dBm/Hz
B=20*10^6;#Hz
Pm=35;#dBm
Qm=6;#seconds
RoadLength=1000;
V_max = 20; # m/sec;
U = 120; # m/sec
v_0 = 4.03;#Mean rotor induced velocity in hover
c_0 = 0.6;#Fuselage drag ratio
epsilon = 1.225; #kg/m^3
r = 0.05;#Rotor solidity
A = 0.503; #m^2
k = 10^(-28); #coefficient


# TASK GENERATION
m=1
tau=1000 #simulation time
lam=1/tau 
task_arrival=np.random.poisson(lam,tau)
print(task_arrival.shape)
print(np.sum(task_arrival))

def TaskGenerator(runtime,num_event):
    task_arrival=np.random.poisson(num_event/runtime,runtime)
    return task_arrival

### CAVS
car_rate=.2
sim_runtime=tau
car_arrivals=np.random.poisson(car_rate,sim_runtime)
print("car_arrivals\n",car_arrivals)
print("car_arrivals.shape\n",car_arrivals.shape)
print("np.sum(car_arrivals)\n",np.sum(car_arrivals))

#monte carlo test
monte=[]
for index in range(10000):
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

cav_number=np.sum(car_arrivals)
indices_of_arrivals=np.where(car_arrivals==1)[0]
CAVs=np.array([CAV() for index,arrival in enumerate(indices_of_arrivals)])
print("indices_of_arrivals\n",indices_of_arrivals)
for index,arrival in enumerate(indices_of_arrivals):
    CAVs[index].EnteringTime=arrival
    CAVs[index].LeavingTime=int(arrival+(RoadLength/CAVs[index].Speed))
    CAVs[index].PositionVector=np.zeros(RoadLength)
    for index_ in range(RoadLength):
        if index_ > arrival and index_<CAVs[index].LeavingTime:
            CAVs[index].PositionVector[index_]=CAVs[index].PositionVector[index_-1]+CAVs[index].Speed
    Tasks=TaskGenerator((CAVs[index].LeavingTime-CAVs[index].EnteringTime),1)
    print("index and task",index,Tasks)
    print("nerede",np.where(Tasks > 0)[0]+arrival)
    CAVs[index].TaskTimes = np.where(Tasks > 0)[0] + arrival if np.all(np.where(Tasks > 0)[0] + arrival < 1000) else []
    print("CAV #",index)
    print("Entering Time",CAVs[index].EnteringTime)
    print("Leaving Time",CAVs[index].LeavingTime)
    print("Task Times",CAVs[index].TaskTimes)
    print("Position Vector",CAVs[index].PositionVector)

np.save("./data/CAVs.npy",CAVs)
allTask=np.zeros(1000)
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
def Gain(CAVPos,UAVPos):
    gain=10**(G0/10)/(math.sqrt(H**2+(CAVPos-UAVPos)**2))**2;
    return gain
gain=Gain(220,500)

def UplinkRate(CAVPos,UAVPos):
    gain=Gain(CAVPos,UAVPos)
    rate=math.log2(1+(gain*((10**(Pm/10))/(10**(N0/10)*B))))*B;
    return rate
u_rate=UplinkRate(1000,0)
print("uplink rate",u_rate)


