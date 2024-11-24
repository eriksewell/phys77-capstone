import numpy as np

class Body:

    def __init__(self, mass, position, velocity):
        self.mass = mass # mass of body [kg]
        self.position = np.array(position) # position of body [m]
        self.velocity = np.array(velocity) # velocity of body [m/s]

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

    for i, body1 in enumerate(bodies):
        for j, body2 in enumerate(bodies):
            if j > i: # only calculate upper triangle of skew symmetric matrix
                d = body2.position - body1.position # displacement from body1 to body2
                r = np.linalg.norm(d) # distance between bodies
                if r != 0:
                    U[i, j] = d / r # calculate displacement unit vector between bodies
                    U[j, i] = -U[i, j] # fill skew symmetric matrix
                else:
                    U[i, j] = 0 # avoid division by 0
                    U[j, i] = 0 # avoid division by 0
    
    print(f'X components of displacement unit vectors \n{U[:,:,0]}')
    print(f'Y components of displacement unit vectors \n{U[:,:,1]}')

    return U

def calculate_force(bodies, U):

    G = 1 # Gravitational constant

    

class NBodySimulation:

    # bodies = list of bodies involved in simulation
    def __init__(self, bodies):
        self.constants()
        self.bodies = bodies

    def constants(self):
        self.G = 6.67430e-11 # gravitational constant [N*m^2/kg^2]
        self.c = 3e8 # speed of light [m/s]

    # run simulation