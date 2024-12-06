import numpy as np

class Body:

    def __init__(self, mass, position, velocity):
        self.mass = mass # mass of body [kg]
        self.position = np.array(position, dtype=np.float64) # position of body [m]
        self.velocity = np.array(velocity, dtype=np.float64) # velocity of body [m/s]
        self.force = np.array([0, 0], dtype=np.float64) # force on body [N]

    def calculate_force(self, pos, mass):
        G = 1 # gravitational constant
        soft = 0.1 # softening parameter

        # displacement vector from self to other_body
        r = pos - self.position 

        # force vector on self from other_body
        F = (G * mass * self.mass * r) / ((np.linalg.norm(r) + soft)**3)

        self.force = self.force + F # update force on body

# initialize bodies with random masses, positions, and velocities over set range
# num_bodies [scalar], mass_range [low, high], position_range [low, high], velocity_range [low, high]
def initialize_bodies(num_bodies, mass_range, position_range, velocity_range):

    masses = np.random.uniform(mass_range[0], mass_range[1], num_bodies)
    positions = np.random.uniform(position_range[0], position_range[1], (num_bodies, 2))
    velocities = np.random.uniform(velocity_range[0], velocity_range[1], (num_bodies, 2))

    # returning list of bodies
    return [Body(masses[i], positions[i], velocities[i]) for i in range(num_bodies)]