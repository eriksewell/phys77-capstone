from core import Body

class Node:

#Initializes Nodes. 
#Points should be a list of all bodies within the bounds (as an index)
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

# calculates center of mass of selected points
# passes all bodies in their totality, as well as the indices of the selected bodies
# note: note sure if this works just yet, still working on quadtree generation
    def CoMass(self, bodies, simsize):
        masses = [bodies[i].masses() for i in self.points]
        positions = [bodies[i].positions() for i in self.points] 
        
        Xproducts = masses*positions[0]
        XCoM = Xproducts.sum()/masses.sum()

        Yproducts = masses*positions[1]
        YCoM = Yproducts.sum()/masses.sum()

        return XCoM, YCoM


# bodies should be all of the bodies in the node's quadrant
    def subdivide(self, bodies, nodelist, simsize):
# Detects boundaries for each

        quad1points = []
        quad2points = []
        quad3points = []
        quad4points = []

        # print("subdivide bodies is" + str(bodies))
        # print('scanned points in node' + str(self.points))
        for i in self.points:
            
            if  bodies[i].position[0] <= self.nodeposition[0]:
                if bodies[i].position[1] >= self.nodeposition[1]:
                    # print(str(i) +' sorted into quad1')
                    quad1points.append(i)
                else:
                    # print(str(i) +' sorted into quad3')
                    quad3points.append(i)
            else:
                if bodies[i].position[1] >= self.nodeposition[1]:
                    # print(str(i) +' sorted into quad2')
                    quad2points.append(i)
                else:
                    # print(str(i) +' sorted into quad4')
                    quad4points.append(i)
        

        # quad1bodies = [bodies[i] for i in quad1points]
        # quad2bodies = [bodies[i] for i in quad2points]
        # quad3bodies = [bodies[i] for i in quad3points]
        # quad4bodies = [bodies[i] for i in quad4points]

        # print('quad1bodies'+ str(quad1bodies))
        # print('quad2bodies'+ str(quad2bodies))
        # print('quad3bodies'+ str(quad3bodies))
        # print('quad4bodies'+ str(quad4bodies))

        nodelist.append(Node(quad1points, [self.nodeposition[0]-(simsize/(2**(self.size+1))), self.nodeposition[1]+(simsize/(2**(self.size+1)))], self.size+1))
        self.quad1 = len(nodelist)-1
        nodelist.append(Node(quad2points, [self.nodeposition[0]+(simsize/(2**(self.size+1))), self.nodeposition[1]+(simsize/(2**(self.size+1)))], self.size+1))
        self.quad2 = len(nodelist)-1
        nodelist.append(Node(quad3points, [self.nodeposition[0]-(simsize/(2**(self.size+1))), self.nodeposition[1]-(simsize/(2**(self.size+1)))], self.size+1))
        self.quad3 = len(nodelist)-1
        nodelist.append(Node(quad4points, [self.nodeposition[0]+(simsize/(2**(self.size+1))), self.nodeposition[1]-(simsize/(2**(self.size+1)))], self.size+1))
        self.quad4 = len(nodelist)-1

# checking the quad.
    def checkQuad(self, bodies, nodelist, simsize):
        if len(self.points) == 1 or len(self.points) == 0:
            print('only 1 point in node or no points. Recursion terminated')
            return
        
        if len(self.points) > 1:
            self.subdivide(bodies, nodelist, simsize)
            # print('new node quad 1'+str(nodelist[self.quad1]))
            # print('new node quad 2'+str(nodelist[self.quad2]))
            # print('new node quad 3'+str(nodelist[self.quad3]))
            # print('new node quad 4'+str(nodelist[self.quad4]))

            # print('new recursions')
            nodelist[self.quad1].checkQuad(bodies, nodelist, simsize)
            nodelist[self.quad2].checkQuad(bodies, nodelist, simsize)
            nodelist[self.quad3].checkQuad(bodies, nodelist, simsize)
            nodelist[self.quad4].checkQuad(bodies, nodelist, simsize)

        

# may need to implement some sort of softening, but that comes later
# will probably create some sort of other force-calculation. Will do subdivisions first

    
class Quadtree:
    
# Takes bodies of simulation, and simulation size and generates a quadtree with a list of nodes
# Each node contains the nessecary information in a node, as well as the index numbers of it's children
# bodies is all bodies within the simulation in the bodies data structure
    def __init__(self, bodies, simsize):
        self.bodies = bodies
        self.simsize = simsize
        self.nodelist = [Node(list(range(len(bodies))), [0, 0], 0)]
        
        self.nodelist[0].checkQuad(self.bodies, self.nodelist, self.simsize)
   