import time
start_time = time.time()
import math
import numpy as np
import parameters

CAVs = np.load("data/CAVs.npy", allow_pickle=True)
allTask = np.load("data/allTask.npy")

# PARAMETERS
DIMENSIONS = parameters.Parameters.UAVNumber
GLOBAL_BEST = 0
B_LO = 0
B_HI = parameters.Parameters.RoadLength
POPULATION = parameters.Parameters.ParticleCount
V_MAX = parameters.Parameters.V_max
PERSONAL_C = 1.5
SOCIAL_C = 2.5
CONVERGENCE = 0.01
MAX_ITER = 50

def flyingEnergy():
    b_1 = parameters.Parameters.b_sigma/8*parameters.Parameters.b_p*parameters.Parameters.b_s*parameters.Parameters.b_A*(parameters.Parameters.b_omega**3)*(parameters.Parameters.b_R)**3
    b_2 = (1+parameters.Parameters.b_k)*(parameters.Parameters.b_W)**(3/2)/(math.sqrt(2*parameters.Parameters.b_p*parameters.Parameters.b_A))
    E_f = ( b_1 * (1 + 3*parameters.Parameters.V_max**2/parameters.Parameters.U**2) + b_2 * (math.sqrt(1+parameters.Parameters.V_max**4/(4*parameters.Parameters.v_0**4)) - parameters.Parameters.V_max**2/(2*parameters.Parameters.v_0**2)) + 1/2*parameters.Parameters.c_0*parameters.Parameters.epsilon*parameters.Parameters.r*parameters.Parameters.A*parameters.Parameters.V_max**3 ) * parameters.Parameters.T
    return E_f

def Gain(CAVPos, UAVPos):
    return 10 ** (parameters.Parameters.G0 / 10) / (math.sqrt(parameters.Parameters.H ** 2 + np.sum((CAVPos - UAVPos) ** 2)) ** 2)

def UplinkRate(CAVPos, UAVPos): ###
    gain = Gain(CAVPos, UAVPos)
    return math.log2(1 + (gain * (1000*(10 ** (parameters.Parameters.Pm / 10))/1  / (1000*(10 ** (parameters.Parameters.N0 / 10)) * parameters.Parameters.B)))) * parameters.Parameters.B #### Pm

def UplinkDelay(instance, UAV_positions, CAVs, allTask, UAV_Direction):
    D = 0
    transferredDataSize = 0

    while transferredDataSize <= parameters.Parameters.alpha and instance + D < parameters.Parameters.T:

        transferredDataSize += UplinkRate(
            CAVs[int(allTask[instance + D])].PositionVector[int(instance + D)], 
            UAV_positions+parameters.Parameters.V_max*UAV_Direction
        )
        D += 1

    return D

def CAV_still_on_road(CAV_id, completion_time):
    if completion_time < len(CAVs[CAV_id].PositionVector):
        return CAVs[CAV_id].PositionVector[int(completion_time)] > 0


def cost_function(UAV_positions, UAV_directions, CAVs, allTask, num_uavs):
    UAV_Availability = np.zeros(num_uavs)
    UAV_positions = np.array(UAV_positions)  # Ensure positions are in correct format
    UAV_directions = np.array(UAV_directions)
    E_f = flyingEnergy() * num_uavs
    
    tasks = 0
    finished = 0

    for instance in range(parameters.Parameters.T):
        if allTask[instance] != 0:  # If a task exists
            #print(max(CAVs[].PositionVector))
                        
            # Check if any UAV is available
            for uav_idx in range(num_uavs):
                CAV_id = int(allTask[instance])
                if UAV_Availability[uav_idx] <= instance:  # UAV is free
                    delay = UplinkDelay(instance, UAV_positions[uav_idx], CAVs, allTask, UAV_directions[uav_idx])
                    l_m_p = parameters.Parameters.alpha * parameters.Parameters.C / parameters.Parameters.f
                    total_delay = delay + l_m_p  # Total time UAV is occupied
                    completion_time = instance + total_delay

                    E_m_p = parameters.Parameters.k * parameters.Parameters.f**3 * l_m_p
                    E_f =  E_f + E_m_p


                    #print(total_delay)
                    if E_f <= num_uavs * parameters.Parameters.E_max and total_delay <= parameters.Parameters.Qm:
                       if CAV_still_on_road(CAV_id, completion_time):
                            finished += 1
                            UAV_Availability[uav_idx] = completion_time
                            break
                    else:
                        #print(total_delay)
                        pass
                else:
                    #print("instance:",instance)
                    pass

            tasks += 1
    
    return -(100 * finished / tasks)


class Particle:
    def __init__(self, num_uavs, v_max):
        # Each particle represents a unique solution (positions for all UAVs in 1D)
        self.positions = np.random.uniform(B_LO, parameters.Parameters.RoadLength, num_uavs)  # 1D positions for each UAV
        self.velocities = np.random.uniform(-v_max, v_max, num_uavs)  # 1D velocities for each UAV
        self.best_positions = np.copy(self.positions)  # Best-known positions for this particle
        self.best_cost = float('inf')  # Best cost value for this particle

class Swarm:
    def __init__(self, pop_size, num_uavs, v_max):
        self.particles = []
        self.best_positions = None  # Best global positions for all UAVs
        self.best_cost = float('inf')  # Best global cost

        for _ in range(pop_size):
            particle = Particle(num_uavs, v_max)
            self.particles.append(particle)

            cost = cost_function(particle.positions, np.sign(particle.velocities), CAVs, allTask, num_uavs)
            if cost < self.best_cost:
                self.best_cost = cost
                self.best_positions = np.copy(particle.positions)


def particle_swarm_optimization(num_uavs):
    swarm = Swarm(POPULATION, num_uavs, V_MAX)

    inertia_weight = 0.5
    curr_iter = 0

    while curr_iter < MAX_ITER:
        print(curr_iter)
        for particle in swarm.particles:
            for i in range(num_uavs):
                r1, r2 = np.random.rand(), np.random.rand()
                personal = PERSONAL_C * r1 * (particle.best_positions[i] - particle.positions[i])
                social = SOCIAL_C * r2 * (swarm.best_positions[i] - particle.positions[i])
                particle.velocities[i] = inertia_weight * particle.velocities[i] + personal + social
                particle.velocities[i] = np.clip(particle.velocities[i], -V_MAX, V_MAX)
                particle.positions[i] += particle.velocities[i]
                particle.positions[i] = np.clip(particle.positions[i], 0, parameters.Parameters.RoadLength)
                
                if particle.positions[i] >= parameters.Parameters.RoadLength or particle.positions[i] <= 0:
                    particle.velocities[i] = -1*particle.velocities[i]

            cost = cost_function(particle.positions, np.sign(particle.velocities), CAVs, allTask, num_uavs)

            if cost < swarm.best_cost:
                swarm.best_cost = cost
                swarm.best_positions = np.copy(particle.positions)

        if abs(swarm.best_cost - GLOBAL_BEST) < CONVERGENCE:
            print(f"Converged in {curr_iter} iterations.")
            break
        curr_iter += 1

    print("Best UAV Positions:", swarm.best_positions)
    print("Maximum Success Rate:", -swarm.best_cost)
    return -swarm.best_cost, swarm.best_positions



if __name__ == "__main__":
    particle_swarm_optimization(DIMENSIONS)
print("--- %s seconds ---" % (time.time() - start_time))