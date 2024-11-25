import numpy as np

# Firefly Algorithm
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





# Objective function (replace with your own function)
def objective_function(x):
    return np.sum(x**2)

# Problem dimension
dimension = 3

# Search space bounds
lower_bound = 0
upper_bound = Parameters.RoadLength-1

# Population size
population_size = 50

# Maximum number of iterations
max_iterations = 100

# Initialization
population = lower_bound + (upper_bound - lower_bound) * np.random.rand(population_size, dimension)
fitness = np.apply_along_axis(lambda pos: multiple_function(pos, CAVs, allTask), 1, population)

# Main loop
for iteration in range(max_iterations):

    # Move fireflies towards brighter ones
    alpha = 0.2  # Attraction coefficient
    beta = 1  # Absorption coefficient
    gamma = 1  # Randomization parameter

    for i in range(population_size):
        for j in range(population_size):
            if fitness[j] < fitness[i]:
                distance = np.linalg.norm(population[i] - population[j])
                attractiveness = np.exp(-gamma * distance**2)
                population[i] += alpha * attractiveness * (population[j] - population[i]) + beta * (np.random.rand(dimension) - 0.5)

        # Limit the updated positions within the search space
        population[i] = np.maximum(lower_bound, population[i])
        population[i] = np.minimum(upper_bound, population[i])

    # Evaluate fitness of the updated population
    fitness = np.apply_along_axis(lambda pos: multiple_function(pos, CAVs, allTask), 1, population)

    # Update the best solution and fitness
    best_index = np.argmin(fitness)
    best_solution = population[best_index]
    best_fitness = fitness[best_index]

    # Display the best fitness value at each iteration
    print(f"Iteration {iteration+1}, Best Fitness = {best_fitness}")

# Display the final best solution and fitness
print("-------------------")
print("Optimization Results")
print("-------------------")
print("Best Solution:", best_solution)
print("Best Fitness:", best_fitness)
