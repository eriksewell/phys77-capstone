import numpy as np
import scipy.integrate

class Body:

    def __init__(self, mass, position, velocity):
        self.mass = mass # mass of body [kg]
        self.position = position # position of body [m]
        self.velocity = velocity # velocity of body [m/s]

class NBodySimulation:

    # bodies = list of bodies involved in simulation
    def __init__(self, bodies):
        self.constants()
        self.bodies = bodies

    def constants(self):
        self.G = 6.67430e-11 # gravitational constant [N*m^2/kg^2]
        self.c = 3e8 # speed of light [m/s]

    # run simulation