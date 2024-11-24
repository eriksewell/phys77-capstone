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

def calculate_displacement(bodies):

    # U[i,j,0] = x-component of displacement unit vector from body_i to body_j
    U = np.zeros([len(bodies), len(bodies), 2]) # 3D displacement matrix
    R = np.zeros([len(bodies), len(bodies)]) # 2D distance matrix

    for i, body_i in enumerate(bodies):
        for j, body_j in enumerate(bodies):
            if j > i: # only calculate upper triangle of matrix
                d = body_j.position - body_i.position # displacement from body1 to body2
                r = np.linalg.norm(d) # calculate distance between bodies
                R[i, j] = r # fill upper triangle of distance matrix
                R[j, i] = R[i, j] # fill symmetric matrix
                if r != 0: # avoid division by zero
                    U[i, j] = d / r # calculate displacement unit vector between bodies
                    U[j, i] = -U[i, j] # fill skew symmetric matrix 

    return U, R

def calculate_force(bodies):

    G = 1 # Gravitational constant

    U, R = calculate_displacement(bodies)

    # F[k,m,0] = x-component of force vector on body_m from body_k
    F = np.zeros([len(bodies), len(bodies), 2]) # 3D force matrix

    for k, body_k in enumerate(bodies):
        for m, body_m in enumerate(bodies):
            if m > k: # only calculate upper triangle of matrix
                if R[k,m] != 0: # avoid division by zero
                    F[k, m] = (G * bodies[k].mass * bodies[m].mass / R[m, k]**2) * U[m, k] # calculate force on body_m from body_k
                    F[m, k] = -F[k, m] # fill skew symmetric matrix
    
    return F