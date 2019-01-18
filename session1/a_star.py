# Based on the wiki page and pseudocode : https://en.wikipedia.org/wiki/A*_search_algorithm

import matplotlib as mpl
from matplotlib import pyplot
import numpy as np

class Node:
    # initialise an object NODE characterized by :
    #      pos : position in the grid
    #      statut : state, opened, blocked... (to know which color in the graph)
    #      f : The f score of the node (set to infinity) check the wiki page
    #      g : The g score of the node (also set to infinity) check the wiki page for the formulae
    #      neighbor : the neighbors of that nodes
    def __init__(self,pos_):
        self.pos=pos_
        self.statut='open' 
        self.f=float('inf')
        self.g=float('inf')
        self.neighbors=[]
        
    def check_and_append(self,nb):
        # check if a nieghbor is open and append is so
        if nb.statut is 'open':
            self.neighbors.append(nb)

def dist_between(node1,node2):
    # distance between 2 nodes, catesian way biatch
    x=abs(node1.pos[0]-node2.pos[0])
    y=abs(node1.pos[1]-node2.pos[1])
    return np.sqrt(pow(x,2)+pow(y,2))

class Grid:
    # Grid object composed of
    # grid : a matrix of integer (to show the color)
    # nodegrid :a matrix of node objects
    def __init__(self,_width,_height):
        self.width=_width
        self.height=_height
        self.grid=np.random.randint(1,size=(_width,_height)) # create a 2-D array of 0
        self.nodegrid=[]
        print('New Grid created')

    def addobstacle(self,wh,pos):
        # input : wh : tuple of width and height that determine the block
        #         pos : position of the block
        # add that block on the position of the main grid
        addgrid = np.random.randint(1,2,size=(wh[0],wh[1]))
        for i in range(len(addgrid)):
            for j in range(len(addgrid[i])):
                self.grid[i+pos[0]][j+pos[1]]=(self.grid[i+pos[0]][j+pos[1]]+addgrid[i][j])%2
        print('Obstacle added')

    def cell_to_node(self):
        # Convert the grid on integer into a grid of node objects. 
        # and set the status of the nodes 
        for i in range(self.width):
            templist=[]
            for j in range(self.height):
                n=Node((i,j))
                if self.grid[i][j]==1:
                    n.statut='closed'
                templist.append(n)
            self.nodegrid.append(templist)
        print('Cells converted to nodes')

    def node_to_cell(self):
        # convert grid of nodes into grid of integer, to be "processable"
        # by pyplot that set each int value into a defined color
        print('Converting nodes to cell to show that beauty...')
        for liste in self.nodegrid:
            for node in liste:
                pos=node.pos
                if node.statut=='open':
                    self.grid[pos[0]][pos[1]]=0
                elif node.statut=='closed':
                    self.grid[pos[0]][pos[1]]=1
                elif node.statut=='checked':
                    self.grid[pos[0]][pos[1]]=2
                else:
                    self.grid[pos[0]][pos[1]]=3

    def set_neighbors(self): 
        # link each nodes of a grid with is neighbor.
        # But only in the neighbor is 'opened'
        for i in range(self.width):
            for j in range(self.height):
                current=self.nodegrid[i][j]
                if not i == 0:
                    current.check_and_append(self.nodegrid[i-1][j])
                    if not j == 0:
                        current.check_and_append(self.nodegrid[i-1][j-1])
                    if not j == self.height-1:
                        current.check_and_append(self.nodegrid[i-1][j+1])
                if not i == self.width-1:
                    current.check_and_append(self.nodegrid[i+1][j])
                    if not j == 0:
                        current.check_and_append(self.nodegrid[i+1][j-1])
                    if not j == self.height-1:
                        current.check_and_append(self.nodegrid[i+1][j+1])
                if not j == 0:
                    current.check_and_append(self.nodegrid[i][j-1])
                if not j == self.height-1:
                    current.check_and_append(self.nodegrid[i][j+1])
        print('Neighbors of each nodes are set')



def lowestfof(liste):
    # Return the node that have the lowest f score of an array
    res=None
    winner_score=float('inf')
    for node in liste:
        if node.f < winner_score:
            winner_score=node.f
            res=node
    return res
    
def path_finder(node,cFrom):
    # Check which node come from and then reconstruct
    # the path by set the color of each nodes of that path in green
    while node in cFrom.keys():
        node.statut='colored'
        node=cFrom[node]

def A_Star(start,goal):
    # The A* algorythm. Check the pseudo code in the wiki page
    print('Finding path ...')
    cameFrom={}
    closedSet=[]
    openSet=[]
    start.g=0
    start.f=dist_between(start,goal)
    openSet.append(start)

    while len(openSet)>0:
        current = lowestfof(openSet)
        if current == goal:
            path_finder(current,cameFrom)
            break
        openSet.remove(current)
        closedSet.append(current)
        for neighbor in current.neighbors:
            neighbor.statut='checked'
            if neighbor in closedSet:
                continue
            test_gscore = current.g + dist_between(current,neighbor)
            if neighbor not in openSet:
                openSet.append(neighbor)
            elif test_gscore >= neighbor.g:
                continue
            cameFrom[neighbor]=current
            neighbor.g=test_gscore
            neighbor.f=neighbor.g+dist_between(neighbor,goal)



def show_graph(grid):
    # set pyplot and then show
    cmap = mpl.colors.ListedColormap(['white','black','red','green'])
    bounds=[0,0.5,1.5,2.5,3]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    img = pyplot.imshow(grid,interpolation='nearest',
                    cmap = cmap,norm=norm)

    pyplot.xticks([]), pyplot.yticks([])

    pyplot.show()


# Create a grid and add obstacle into it
grid=Grid(100,100)
grid.addobstacle((10,30),(48,48))
grid.addobstacle((10,80),(15,0))
grid.addobstacle((10,80),(50,20))

grid.addobstacle((70,70),(20,20))
grid.addobstacle((50,50),(40,40))
grid.addobstacle((40,40),(50,50))

# Process the grid to become path findable
grid.cell_to_node()
grid.set_neighbors()

# A* search algorythm
A_Star(grid.nodegrid[0][0],grid.nodegrid[-1][-1])

# Convert the nodes to cells to be readable for pyplot then show
grid.node_to_cell()
show_graph(grid.grid)

