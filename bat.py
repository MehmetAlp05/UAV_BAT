import numpy as np
import math
import matplotlib.pyplot as plt
from parameters import Parameters
CAVs=np.load("./data/CAVs.npy",allow_pickle=True)
allTask=np.load("./data/allTask.npy")
leavingTimes=np.load("./data/leavingTimes.npy")
def Gain(CAVPos,UAVPos):
    gain=10**(Parameters.G0/10)/(math.sqrt(Parameters.H**2+(CAVPos-UAVPos)**2))**2;
    return gain

def UplinkRate(CAVPos,UAVPos):
    gain=Gain(CAVPos,UAVPos)
    rate=math.log2(1+(gain*((10**(Parameters.Pm/10))/(10**(Parameters.N0/10)*Parameters.B))))*Parameters.B;
    return rate
def UplinkDelay(instance,UAV_position,CAVs,allTask,UAV_direction):
    UplinkRate(CAVs[int(allTask[instance])].PositionVector[int(instance)],UAV_position)
    D=0;
    transferredDataSize=0;
    while transferredDataSize<=Parameters.alpha and instance+D<Parameters.T:
        transferredDataSize=transferredDataSize+UplinkRate(CAVs[int(allTask[instance+D])].PositionVector[int(instance+D)],UAV_position+Parameters.UAVSpeed*UAV_direction);
        D=D+1;
    return D
def simulation(startPosition,startDirection,CAVs,allTask):
    UAV_position=startPosition
    UAV_direction=startDirection
    queue=[]
    tasks=[]
    finished=0
    #print(Parameters.T)
    for instance in range(Parameters.T):
        #add taks
        if allTask[instance]!=0:
            delay=UplinkDelay(instance,UAV_position,CAVs,allTask,UAV_direction)
            #print(delay)
            if delay<6:
                finished+=1
            tasks=np.append(tasks,allTask[instance])
        if UAV_position+Parameters.UAVSpeed*UAV_direction>1000 or UAV_position+Parameters.UAVSpeed*UAV_direction<0:
            UAV_direction*=-1
        UAV_position+=Parameters.UAVSpeed*UAV_direction
        #print("UAV_position@",instance,"is",UAV_position)
    #print("tasks",len(tasks))
    #print("finished",finished)
    #print("succces ratio is %",100*finished/len(tasks))
    return -(100*finished/len(tasks))
simulation(300,1,CAVs,allTask)
#print("task number is",len(allTask[allTask!=0]))
#print(allTask.shape)
# replace this 
def sphere_function(x):
    return np.sum(x**2)

# Parameters
num_bats = 5
dim = 1
num_iterations = 100
freq_min = 0
freq_max = 2
A = 0.5
r0 = 0.5
alpha = 0.9
gamma = 0.9
lb = 0
ub = 999

# Initialize bat positions and velocities
positions = np.random.uniform(lb, ub, (num_bats, dim))
velocities = np.zeros((num_bats, dim))
frequencies = np.zeros(num_bats)
loudness = A * np.ones(num_bats)
pulse_rate = r0 * np.ones(num_bats)

# Evaluate initial fitness
fitness = np.apply_along_axis(lambda pos: simulation(pos, -1, CAVs, allTask), 1, positions)
best_position = positions[np.argmin(fitness)]
best_fitness = np.min(fitness)

for iteration in range(num_iterations):
    avg_loudness = np.mean(loudness)
    avg_pulse_rate = np.mean(pulse_rate)
    
    # Update bats
    for i in range(num_bats):
        beta = np.random.uniform(0, 1)
        frequencies[i] = freq_min + (freq_max - freq_min) * beta
        velocities[i] += (positions[i] - best_position) * frequencies[i]
        new_position = positions[i] + velocities[i]
        
        # Boundary check
        new_position = np.clip(new_position, lb, ub)
        
        # Local search
        if np.random.uniform(0, 1) > pulse_rate[i]:
            epsilon = np.random.uniform(-1, 1)
            new_position = positions[i] + epsilon * avg_loudness
        
        # Evaluate new solution
        new_fitness = simulation(new_position,1,CAVs,allTask)
        
        # Greedy mechanism to update if new solution is better and random value is less than loudness
        if new_fitness < fitness[i] and np.random.uniform(0, 1) < loudness[i]:
            positions[i] = new_position
            fitness[i] = new_fitness
            
        # Update global best
        if fitness[i] < best_fitness:
            best_position = positions[i]
            best_fitness = fitness[i]
            
        loudness[i] *= alpha
        pulse_rate[i] = r0 * (1 - np.exp(-gamma * iteration))
            
    # Print the best fitness value in each iteration
    print(f"Iteration {iteration + 1}: Best Fitness = {best_fitness}")

print("\nOptimized Solution:", best_position)
print("Best Fitness Value:", best_fitness)