from core import Body
import numpy as np

class Node:

#Initializes Nodes. 
#Points should be a list of the indices of the bodies within the node
#Measure position of nodes from center of the node
#size should be an integer. will determine size of the nodes based upon a fraction of the total size: e.g. (n/2**size)
    def __init__(self, points, nodeposition, size):
        self.points = points
        self.nodeposition = nodeposition
        self.size = size
        self.quad1 = None
        self.quad2 = None
        self.quad3 = None
        self.quad4 = None

# calculates the center of mass and total mass of all bodies in current node
    def find_CoM(self, bodies):

        if len(self.points) != 0:
            # Calculates total mass of node
            Mass = sum(bodies[i].mass for i in self.points)
            # calculate center of mass of node
            CoM = sum(bodies[i].mass * bodies[i].position for i in self.points) / Mass

            return CoM, Mass
        else:
            return None, 0
        
# passed variable "bodies" should be all of the bodies in the node's quadrant
# passed variable "nodelist" is the list of nodes within the quadtree, and is passed to the function for every recursion
# simsize is consistent, and is modified based on the size of the node
    def subdivide(self, bodies, nodelist, simsize):

# Detects boundaries for each quadrant and sorts the bodies accordingly
        quad1points = []
        quad2points = []
        quad3points = []
        quad4points = []

        for i in self.points:
            
            if  bodies[i].position[0] <= self.nodeposition[0]:
                if bodies[i].position[1] >= self.nodeposition[1]:
                    quad1points.append(i)
                else:
                    quad3points.append(i)
            else:
                if bodies[i].position[1] >= self.nodeposition[1]:
                    quad2points.append(i)
                else:
                    quad4points.append(i)
                    
# Quad points => [1] [2]
#             => [3] [4]
# Appends new child nodes to the nodelist
# Existing parent node is given the indices to the child node within the nodelist
        nodelist.append(Node(quad1points, [self.nodeposition[0]-(simsize/(2**(self.size+1))), self.nodeposition[1]+(simsize/(2**(self.size+1)))], self.size+1))
        self.quad1 = len(nodelist)-1
        nodelist.append(Node(quad2points, [self.nodeposition[0]+(simsize/(2**(self.size+1))), self.nodeposition[1]+(simsize/(2**(self.size+1)))], self.size+1))
        self.quad2 = len(nodelist)-1
        nodelist.append(Node(quad3points, [self.nodeposition[0]-(simsize/(2**(self.size+1))), self.nodeposition[1]-(simsize/(2**(self.size+1)))], self.size+1))
        self.quad3 = len(nodelist)-1
        nodelist.append(Node(quad4points, [self.nodeposition[0]+(simsize/(2**(self.size+1))), self.nodeposition[1]-(simsize/(2**(self.size+1)))], self.size+1))
        self.quad4 = len(nodelist)-1

# Recursive function that checks whether a quadrant has multiple bodies. If it does, runs subdivide. If not, ends that section of the recursion
# Passed "bodies" variable is all bodies within
    def checkQuad(self, bodies, nodelist, simsize):

        # Re-check traverse logic for leaf nodes with more than one body to ensure this works
        if simsize / (2**self.size) < 0.01:  # Avoid small quadrants
            return

# If this part ever breaks in the future, just make it so that len(self.points) == 1 or len(self.points) == 0
        if len(self.points) <= 1 :

            return
        
        if len(self.points) > 1:

            self.subdivide(bodies, nodelist, simsize)

# Calls itself recursively
            nodelist[self.quad1].checkQuad(bodies, nodelist, simsize)
            nodelist[self.quad2].checkQuad(bodies, nodelist, simsize)
            nodelist[self.quad3].checkQuad(bodies, nodelist, simsize)
            nodelist[self.quad4].checkQuad(bodies, nodelist, simsize)


class Quadtree:
    
# Takes bodies of simulation, and simulation size and generates a quadtree with a list of nodes
# Each node contains the nessecary information in a node, as well as the index numbers of it's children
# bodies is all bodies within the simulation in the bodies data structure
    def __init__(self, bodies, simsize):
        self.bodies = bodies
        self.simsize = simsize
        self.nodelist = [Node(list(range(len(bodies))), [0, 0], 1)]
        
        self.nodelist[0].checkQuad(self.bodies, self.nodelist, self.simsize)

    # determine if ratio of node size to distance satisfies threshold for approximation
    def check_distance(self, node_index, body_index):

        theta = 0.5 # simulation accuracy parameter

        CoM, Mass = self.nodelist[node_index].find_CoM(self.bodies)

        if CoM is None:
            return False
        
        dimension = self.simsize / 2**(self.nodelist[node_index].size-1) # dimension of node region
        distance = np.linalg.norm(self.bodies[body_index].position - CoM) # distance from body to CoM of node

        if dimension / distance < theta:
            return True
        
        else:
            return False
        
    # determine if the current node contains the body we are calculating forces on
    def contains_self(self, node_index, body_index):

        if body_index in self.nodelist[node_index].points:
            return True
        
        else:
            return False

    # Traverse the quadtree and calculate forces
    def traverse_quadtree(self, node_index, body_index):
        
        # Check if body is in current node
        if self.contains_self(node_index, body_index):

            # Check if current node has children
            if self.nodelist[node_index].quad1 is not None:

                self.traverse_quadtree(self.nodelist[node_index].quad1, body_index)
                self.traverse_quadtree(self.nodelist[node_index].quad2, body_index)
                self.traverse_quadtree(self.nodelist[node_index].quad3, body_index)
                self.traverse_quadtree(self.nodelist[node_index].quad4, body_index)

            # Current node has no children
            else:
                return # Current node only contains self
            
        # Body not in current node
        else:
            if self.check_distance(node_index, body_index):
                # Calculate force on group here
                CoM, Mass = self.nodelist[node_index].find_CoM(self.bodies)
                self.bodies[body_index].calculate_force(CoM, Mass)

            # Current node fails distance check
            else:
                if self.nodelist[node_index].quad1 is not None:

                    self.traverse_quadtree(self.nodelist[node_index].quad1, body_index)
                    self.traverse_quadtree(self.nodelist[node_index].quad2, body_index)
                    self.traverse_quadtree(self.nodelist[node_index].quad3, body_index)
                    self.traverse_quadtree(self.nodelist[node_index].quad4, body_index)

                # Current node has no children
                else:
                    if len(self.nodelist[node_index].points) == 0:
                        # Current node is empty
                        return
                    else:     
                        # Calculate force on bodies in leaf node here
                        for point in self.nodelist[node_index].points:
                            self.bodies[body_index].calculate_force(self.bodies[point].position, self.bodies[point].mass)
                        
