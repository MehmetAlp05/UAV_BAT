import time
start_time = time.time()
import numpy as np
import math
import os
import json  # For saving data in JSON format
from datetime import datetime
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
    finished=[]
    #print(Parameters.T)
    for instance in range(Parameters.T):
        #add taks
        if allTask[instance]!=0:
            delay=UplinkDelay(instance,UAV_position,CAVs,allTask,UAV_direction)
            #print(delay)
            if delay<6:
                finished=np.append(finished,instance)
            tasks=np.append(tasks,allTask[instance])
        if UAV_position+Parameters.UAVSpeed*UAV_direction>1000 or UAV_position+Parameters.UAVSpeed*UAV_direction<0:
            UAV_direction*=-1
        UAV_position+=Parameters.UAVSpeed*UAV_direction
        #print("UAV_position@",instance,"is",UAV_position)
    #print("tasks",len(tasks))
    #print("finished",finished)
    #print("succces ratio is %",100*finished/len(tasks))
    return finished
simulation(300,1,CAVs,allTask)
print(np.count_nonzero(allTask))
def multiple_function(pos,CAVs,allTask):
    task_matrix=np.zeros((len(pos),np.count_nonzero(allTask)))
    #print(np.shape(task_matrix))
    for i in range(len(pos)):
        result=simulation(pos[i],1,CAVs,allTask)
        task_matrix[i,0:len(result)]=result
    #print(task_matrix)
    unique=np.unique(task_matrix[task_matrix!=0])
    return -len(unique)/np.count_nonzero(allTask)
score=multiple_function([999,999],CAVs,allTask)
print("score",score)
#print("task number is",len(allTask[allTask!=0]))
#print(allTask.shape)
# replace this 
def sphere_function(x):
    return np.sum(x**2)

# Parameters
num_bats = 10
dim = 4
num_iterations = 50
freq_min = 0
freq_max = 3
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
fitness = np.apply_along_axis(lambda pos: multiple_function(pos, CAVs, allTask), 1, positions)
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
        new_fitness = multiple_function(new_position,CAVs,allTask)
        
        # Greedy mechanism to update if new solution is better and random value is less than loudness
        if new_fitness < fitness[i] and np.random.uniform(0, 1) < loudness[i]:
            positions[i] = new_position
            fitness[i] = new_fitness
            
        # Update global best
        if fitness[i] < best_fitness:
            best_position = positions[i]
            best_fitness = fitness[i]
            print("new position")
            
        loudness[i] *= alpha
        pulse_rate[i] = r0 * (1 - np.exp(-gamma * iteration))
            
    # Print the best fitness value in each iteration
    print(f"Iteration {iteration + 1}: Best Fitness = {best_fitness}")

print("\nOptimized Solution:", best_position)
print("Best Fitness Value:", best_fitness)

simulation_data={
    "data_rate(mbit)":Parameters.alpha,
    "simulation_runtime(seconds)":Parameters.T,
    "road_length":Parameters.RoadLength,
    "best_position":best_position.tolist(),
    "best_fitness":best_fitness,
    "UAV_number":dim,
    "iteration_number":num_iterations,
    "bat_number":num_bats,
    #"timestamp": datetime.now().isoformat(),  # Add a unique timestamp for tracking
    "cpu_capacity":Parameters.C,
    "transmission_power":Parameters.Pm,
    "uav_altitude":Parameters.H
}
# Directory to save the final result
output_dir = "simulation_results"
os.makedirs(output_dir, exist_ok=True)
# Save all data at the end
output_file = os.path.join(output_dir, "final_results.json")
# Check if the file exists and load existing data
if os.path.exists(output_file):
    with open(output_file, "r") as f:
        try:
            existing_data = json.load(f)
            if isinstance(existing_data, dict):
                # Convert the single dictionary to a list
                existing_data = [existing_data]
            elif not isinstance(existing_data, list):
                raise ValueError("Unexpected JSON structure in the file.")
        except json.JSONDecodeError:
            # File exists but is empty or invalid
            existing_data = []
else:
    existing_data = []

# Append the new simulation run
existing_data.append(simulation_data)

# Save the updated data back to the file
with open(output_file, "w") as f:
    json.dump(existing_data, f, indent=4)

print(f"New simulation results appended to {output_file}.")
print("--- %s seconds ---" % (time.time() - start_time))