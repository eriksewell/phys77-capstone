import numpy as np
from core import Body
from core import 

class Node:

#Initializes Nodes. 
#Points should be a list of all bodies within the bounds
#Measure position of nodes from center of the node
#size should be an integer. will determine size of the nodes based upon a fraction of the total size: e.g. (n/2^size)
    def __init__(self, points, nodeposition, size):
        self.points = points
        self.nodeposition = nodeposition
        self.size = size
        self.quad1 = None
        self.quad2 = None
        self.quad3 = None
        self.quad4 = None

# calculates center of mass of selected points
# passes all bodies in their totality, as well as the indices of the selected bodies
    def CoMass(self, bodies, simsize):
        masses = [bodies[i].masses() for i in self.points]
        positions = [bodies[i].positions() for i in self.points] 
        
        Xproducts = masses*positions[0]
        XCoM = Xproducts.sum()/masses.sum()

        Yproducts = masses*positions[1]
        YCoM = Yproducts.sum()/masses.sum()

        return XCoM, YCoM

    def subdivide(self, bodies):

        quad1points = []
        quad2points = []
        quad3points = []
        quad4points = []
        
# Detects boundaries for each
        for i in self.points:
            if bodies[i].position[0] >= nodeposition[0]:
                if bodies[i].position[1] >= nodeposition[1]:
                    quad1points.append(i)
                else:
                    quad3points.append(i)
            else:
                if bodies[i].position[1] >= nodeposition[1]:
                    quad2points.append(i)
                else:
                    quad4points.append(i)

# Make it node ids to nodes rather than the nodes themselves. Will append nodes to nodelist instead
        self.quad1 = Node(quad1points, [self.nodeposition[0]-(simsize/2**self.size+1),self.nodeposition[1]]+(simsize/2**self.size+1), self.size+1)
        self.quad2 = Node(quad2points, [self.nodeposition[0]+(simsize/2**self.size+1),self.nodeposition[1]]+(simsize/2**self.size+1), self.size+1)
        self.quad3 = Node(quad3points, [self.nodeposition[0]-(simsize/2**self.size+1),self.nodeposition[1]]-(simsize/2**self.size+1), self.size+1)
        self.quad4 = Node(quad4points, [self.nodeposition[0]+(simsize/2**self.size+1),self.nodeposition[1]]-(simsize/2**self.size+1), self.size+1)

# may need to implement some sort of softening, but that comes later
    def forcecalc(self, distantpoint, bodies, simsize):
        
        theta = 1

        if (simsize/2**self.size)/np.linalg.norm(distantpoint-self.nodeposition) < theta:
            # need force calculation formula here
        else:
            self.subdivide(bodies)
            self.quad1.forcecalc(distantpoint, bodies, simsize)
            self.quad2.forcecalc(distantpoint, bodies, simsize)
            self.quad3.forcecalc(distantpoint, bodies, simsize)
            self.quad4.forcecalc(distantpoint, bodies, simsize)

    
class Quadtree:
    
    def __init__(bodies, simsize)
        self.bodies = bodies
        self.simsize = simsize
        self.nodelist = [Node(len(bodies.masses), [simsize/2, simsize/2], 0)]


    def addNode()