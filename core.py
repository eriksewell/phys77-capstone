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

class NBodySimulation:

    # bodies = list of bodies involved in simulation
    def __init__(self, bodies):
        self.constants()
        self.bodies = bodies

    def constants(self):
        self.G = 6.67430e-11 # gravitational constant [N*m^2/kg^2]
        self.c = 3e8 # speed of light [m/s]

    # run simulation