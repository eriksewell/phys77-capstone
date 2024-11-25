import numpy as np

class Body:

    def __init__(self, mass, position, velocity):
        self.mass = np.float64(mass) # mass of body [kg]
        self.position = np.array(position, dtype=np.float64) # position of body [m]
        self.velocity = np.array(velocity, dtype=np.float64) # velocity of body [m/s]

# initialize bodies with random masses, positions, and velocities over set range
# num_bodies [scalar], mass_range [low, high], position_range [low, high], velocity_range [low, high]
def initialize_bodies(num_bodies, mass_range, position_range, velocity_range):

    masses = np.random.uniform(mass_range[0], mass_range[1], num_bodies)
    positions = np.random.uniform(position_range[0], position_range[1], (num_bodies, 2))
    velocities = np.random.uniform(velocity_range[0], velocity_range[1], (num_bodies, 2))

    # returning list of bodies
    return [Body(masses[i], positions[i], velocities[i]) for i in range(num_bodies)]


def calculate_force(bodies):

    G = 1 # gravitational constant
    soft = 0.05 # softening parameter

    F = np.zeros((len(bodies), 2)) # initialize net force array

    for i, body_i in enumerate(bodies):
        for j, body_j in enumerate(bodies):
            if i != j: # avoid self force calculation
                # displacement vector from body_i to body_j
                r_ji = bodies[j].position - bodies[i].position 
                # force vector on body_i from body_j
                F_ij = (G * bodies[i].mass * bodies[j].mass * r_ji) / ((np.linalg.norm(r_ji) + soft)**3)
                F[i] += F_ij # calculate net force on body_i
    
    return F