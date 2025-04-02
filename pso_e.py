import numpy as np
import math
import os
import json  # For saving data in JSON format
from datetime import datetime
import matplotlib.pyplot as plt
from parameters import Parameters

#--------------------------------------------------------
#add data
CAVs=np.load("./data/CAVs.npy",allow_pickle=True)
allTask=np.load("./data/allTask.npy")
leavingTimes=np.load("./data/leavingTimes.npy")
#functions
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

def ProcessDelay():
    return Parameters.alpha*Parameters.C/Parameters.f
def Energy():
    b_1 = Parameters.b_sigma/8*Parameters.b_p*Parameters.b_s*Parameters.b_A*(Parameters.b_omega**3)*(Parameters.b_R)**3;
    b_2 = (1+Parameters.b_k)*(Parameters.b_W)**(3/2)/(math.sqrt(2*Parameters.b_p*Parameters.b_A));
    E_f = ( b_1 * (1 + 3*Parameters.V_max**2/Parameters.U**2) + b_2 * (math.sqrt(1+Parameters.V_max**4/(4*Parameters.v_0**4)) - Parameters.V_max**2/(2*Parameters.v_0**2)) + 1/2*Parameters.c_0*Parameters.epsilon*Parameters.r*Parameters.A*Parameters.V_max**3 ) * Parameters.T
    #print("Emax=",Parameters.E_max,"E_f=",E_f)
    E_pm_t = (Parameters.k * Parameters.f**2)*Parameters.alpha*Parameters.C
    #print("processing energy per second, ",E_pm_t*98)
    left=(Parameters.E_max-E_f)/E_pm_t
    #print("total processing energy after flying",left)
    return E_pm_t,E_f,Parameters.E_max

def simulation(startPosition,startDirection,CAVs,allTask):
    E_pm_t,E_f,E_max=Energy()
    battery=E_max-E_f
    UAV_position=startPosition
    UAV_direction=startDirection
    queue=0
    tasks=[]
    finished=[]
    #print(Parameters.T)
    for instance in range(Parameters.T):
        #add taks
        if battery<0:
            break
        if allTask[instance]!=0:
            #delay=UplinkDelay(queue+instance,UAV_position+Parameters.UAVSpeed*UAV_direction*queue,CAVs,allTask,UAV_direction)+Parameters.alpha*Parameters.C/Parameters.f
            delay=UplinkDelay(instance,UAV_position+Parameters.UAVSpeed*UAV_direction*queue,CAVs,allTask,UAV_direction)+Parameters.alpha*Parameters.C/Parameters.f
            #print(delay)
            if delay<=Parameters.Qm:
                queue+=delay
                finished=np.append(finished,instance)
            tasks=np.append(tasks,allTask[instance])
        if UAV_position+Parameters.UAVSpeed*UAV_direction>Parameters.RoadLength or UAV_position+Parameters.UAVSpeed*UAV_direction<0:
            UAV_direction*=-1
        UAV_position+=Parameters.UAVSpeed*UAV_direction
        if queue>0:
            queue-=1
            battery-=E_pm_t
        #print("UAV_position@",instance,"is",UAV_position)
    #print("tasks",len(tasks))
    #print("finished",finished)
    #print("succces ratio is %",100*finished/len(tasks))
    return finished
example_sim=simulation(0,1,CAVs,allTask)
print(len(example_sim))
#print(allTask)
print("total task",np.count_nonzero(allTask))
print(len(example_sim)/np.count_nonzero(allTask))

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

#--------------------------------------------------------
# PSO Parameters
numParticles = 20  # Number of particles in the swarm
maxIterations = 50  # Maximum number of iterations
c1 = 2  # Cognitive coefficient
c2 = 2  # Social coefficient
w = 0.7  # Inertia weight

# Problem-specific parameters
Dim = 1  # Dimensionality of the problem
# Define your problem here, including the objective function and any constraints
lb = 0
ub = Parameters.RoadLength-1

# Define the PSO function
def pso():
    # Initialize the swarm
    position = np.random.uniform(lb, ub, (numParticles, Dim))  # Particle positions
    velocity = np.zeros((numParticles, Dim))  # Particle velocities
    personalBest = position.copy()  # Personal best positions
    personalBestFitness = np.zeros(numParticles) + np.inf  # Personal best fitness values
    globalBest = np.zeros(Dim)  # Global best position
    globalBestFitness = np.inf  # Global best fitness value

    # Main loop
    for iteration in range(maxIterations):
        # Evaluate fitness for each particle
        fitness = np.apply_along_axis(lambda pos: multiple_function(pos, CAVs, allTask), 1, position)
        for i in range(numParticles):
            # Update personal best if better fitness is found
            if fitness[i] < personalBestFitness[i]:
                personalBest[i] = position[i]
                personalBestFitness[i] = fitness[i]

            # Update global best if better fitness is found
            if fitness[i] < globalBestFitness:
                globalBest = position[i]
                globalBestFitness = fitness[i]

        # Update particle velocities and positions
        for i in range(numParticles):
            r1 = np.random.rand(Dim)
            r2 = np.random.rand(Dim)
            velocity[i] = w * velocity[i] \
                          + c1 * r1 * (personalBest[i] - position[i]) \
                          + c2 * r2 * (globalBest - position[i])
            print(position[i])
            print(velocity[i])
            print(position+velocity[i])

            if (position[i] + velocity[i]).all()>lb and (position[i] + velocity[i]).all()<ub:
                position[i] = position[i] + velocity[i]

            # Apply any necessary constraints to the particle positions

            # Update fitness if necessary

            # Display current best fitness
            print(f'Iteration {iteration + 1}: Best Fitness = {globalBestFitness}')

    # Display final result
    print('Optimization Complete!')
    print(f'Best Fitness = {globalBestFitness}')
    print(f'Best Position = {globalBest}')

    best_fitness=globalBestFitness
    best_position=globalBest
    dim=Dim
    simulation_data={
    "data_rate(mbit)":Parameters.alpha,
    "simulation_runtime(seconds)":Parameters.T,
    "road_length":Parameters.RoadLength,
    "best_position":best_position.tolist(),
    "best_fitness":best_fitness,
    "UAV_number":dim,
    #"timestamp": datetime.now().isoformat(),  # Add a unique timestamp for tracking
    "computing_power":Parameters.f,
    "transmission_power":Parameters.Pm,
    "uav_altitude":Parameters.H
    }
    # Directory to save the final result
    output_dir = "pso_results"
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

# Define your objective function
def objective_function(x):
    # Define your objective function here
    pass


# Run the PSO algorithm
pso()
