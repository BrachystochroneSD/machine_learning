# Based on the wiki page and pseudocode : https://en.wikipedia.org/wiki/A*_search_algorithm and backtracking maze generator

import matplotlib as mpl
from matplotlib import pyplot
import numpy as np
import random

class Node:
    def __init__(self,pos_):
        self.pos=pos_
        self.statut='open'
        self.f=float('inf')
        self.g=float('inf')
        self.neighbors=[]
        self.links=[]

    def check_and_append(self,nb):
        if nb.statut is 'open':
            self.neighbors.append(nb)

def dist_between(node1,node):
    # distance between 2 nodes catesian way
    x=abs(node1.pos[0]-node.pos[0])
    y=abs(node1.pos[1]-node.pos[1])
    return np.sqrt(pow(x,2)+pow(y,2))

class Grid:

    def __init__(self,_width,_height):
        self.width=_width
        self.height=_height
        self.grid=np.random.randint(1,2,size=(_width*2+1,_height*2+1))
        self.nodegrid=[]
        self.unvisitednodes=[]
        print('New Grid created')

    def addobstacle(self,wh,pos):
        addgrid = np.random.randint(1,2,size=(wh[0],wh[1]))
        for i in range(len(addgrid)):
            for j in range(len(addgrid[i])):
                self.grid[i+pos[0]][j+pos[1]]=(self.grid[i+pos[0]][j+pos[1]]+addgrid[i][j])%2
        print('Obstacle added')

    def cell_to_node(self):
        for i in range(self.width):
            templist=[]
            for j in range(self.height):
                n=Node((i,j))
                self.grid[i*2+1][j*2+1]==0
                # if self.grid[i*2+1][j*2+1]==1:
                #     n.statut='closed'
                templist.append(n)
                self.unvisitednodes.append(n)
            self.nodegrid.append(templist)
        print('Cells converted to nodes')

    def node_to_cell(self):
        print('Path found! Converting nodes to cell to show that beauty...')
        for liste in self.nodegrid:
            for node in liste:
                pos=node.pos
                if node.statut=='open':
                    self.grid[pos[0]*2+1][pos[1]*2+1]=0
                elif node.statut=='closed':
                    self.grid[pos[0]*2+1][pos[1]*2+1]=1
                elif node.statut=='checked':
                    self.grid[pos[0]*2+1][pos[1]*2+1]=2
                else:
                    self.grid[pos[0]*2+1][pos[1]*2+1]=3

    def set_neighbors(self):
        for i in range(self.width):
            for j in range(self.height):
                current=self.nodegrid[i][j]
                if not i == 0:
                    current.check_and_append(self.nodegrid[i-1][j])
                if not i == self.width-1:
                    current.check_and_append(self.nodegrid[i+1][j])
                if not j == 0:
                    current.check_and_append(self.nodegrid[i][j-1])
                if not j == self.height-1:
                    current.check_and_append(self.nodegrid[i][j+1])
        print('Neighbors of each nodes are set')



def lowestfof(liste):
    res=None
    winner_score=float('inf')
    for node in liste:
        if node.f < winner_score:
            winner_score=node.f
            res=node
    return res

def path_finder(node,cFrom):
    while node in cFrom.keys():
        node.statut='colored'
        colorlink(node,cFrom[node],3)
        node=cFrom[node]

def A_Star(start,goal):
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
        for neighbor in current.links:
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
    cmap = mpl.colors.ListedColormap(['#fbf1c7','#282828','#9d0006','#458588'])
    bounds=[0,0.5,1.5,2.5,3]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    img = pyplot.imshow(grid,interpolation='nearest',
                    cmap = cmap,norm=norm)
    pyplot.xticks([]), pyplot.yticks([])

    pyplot.show()

def take_random_of(array):
    index=random.randint(0,len(array)-1)
    return array[index]

def take_unvisited_nb(neighbors,nodelist):
    res=[]
    for nb in neighbors:
        if nb in nodelist:
            res.append(nb)
    return res

def addlink(node1,node2,grid):
    node1.links.append(node2)
    node2.links.append(node1)
    colorlink(node1,node2,0)

def colorlink(node1,node2,col):
    i=int(((node1.pos[0]*2+1)+(node2.pos[0]*2+1))/2)
    j=int(((node1.pos[1]*2+1)+(node2.pos[1]*2+1))/2)
    grid.grid[i][j]=col


def maze_gen(start_cell,visit_list,grid):
    print('Creating a maze ...')
    current=start_cell
    stack=[]
    visit_list.remove(current)
    while len(visit_list)>0:
        un_nb=take_unvisited_nb(current.neighbors,visit_list)
        if len(un_nb)>0:
            rand_nb=take_random_of(un_nb)
            stack.append(current)
            addlink(current,rand_nb,grid)
            current=rand_nb
            visit_list.remove(current)
        elif len(stack)>0:
            current=stack.pop()



# w=np.random.randint(1,500)
# h=np.random.randint(1,500)
w=30
h=30
print('creating grid for '+str(w)+' '+str(h))
grid=Grid(w,h)
# Process the grid to become path findable
grid.cell_to_node()
grid.set_neighbors()


# Generate a maze from the grid
maze_gen(grid.nodegrid[0][0],grid.unvisitednodes,grid)



# Set the position of the start an end in the maze
s_pos=0,0
e_pos=-1,-1
# s_pos=np.random.randint(w-1),np.random.randint(h-1)
# e_pos=np.random.randint(w-1),np.random.randint(h-1)

# A* search algorythm
A_Star(grid.nodegrid[s_pos[0]][s_pos[1]],grid.nodegrid[e_pos[0]][e_pos[1]])

# Convert the nodes to cells to be readable for pyplot then show
grid.node_to_cell()
show_graph(grid.grid)
