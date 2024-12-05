from core import Body

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

# calculates the center of mass of all bodies within the node
    def CoM(self, bodies):

        if len(self.points) != 0:
            # calculate center of mass of node
            CoM = sum(bodies[i].mass * bodies[i].position for i in self.points) / sum(bodies[i].mass for i in self.points)

            return CoM
        else:
            return
        
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
   