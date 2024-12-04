import numpy as np

class Body:

    def __init__(self, mass, position, velocity):
        self.mass = mass # mass of body [kg]
        self.position = np.array(position) # position of body [m]
        self.velocity = np.array(velocity) # velocity of body [m/s]
        self.force = np.array([0, 0]) # force on body [N]

    def calculate_force(self, other_body):
        G = 1 # gravitational constant
        soft = 0.05 # softening parameter

        # displacement vector from self to other_body
        r = other_body.position - self.position 

        # force vector on self from other_body
        F = (G * other_body.mass * self.mass * r) / ((np.linalg.norm(r) + soft)**3)

        return F # return force vector on self from other_body

# initialize bodies with random masses, positions, and velocities over set range
# num_bodies [scalar], mass_range [low, high], position_range [low, high], velocity_range [low, high]
def initialize_bodies(num_bodies, mass_range, position_range, velocity_range):

    masses = np.random.uniform(mass_range[0], mass_range[1], num_bodies)
    positions = np.random.uniform(position_range[0], position_range[1], (num_bodies, 2))
    velocities = np.random.uniform(velocity_range[0], velocity_range[1], (num_bodies, 2))

    # returning list of bodies
    return [Body(masses[i], positions[i], velocities[i]) for i in range(num_bodies)]