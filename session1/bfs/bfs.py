import json
from collections import deque

data=[]
filee=open('/home/samrenfou/Dropbox/neural_network/breathd_shit/data.json').read()
json=json.loads(filee)

class Node():
    def __init__(self, value):
        self.value=value
        self.links=[]
        self.parent=[]
        self.visited=False
        
    def addLinks(self,node):
        self.links.append(node)
        node.links.append(self)
        
class Graph():
    
    def __init__(self):
        self.nodes=[]
        self.graph={}
        self.end=None
        self.start=None

    def addNode(self,node):
        self.nodes.append(node)
        self.graph[node.value]=node

    def isinGraph(self,node):
        res=False
        for nodecheck in self.nodes:
            if(node.value==nodecheck.value):
                res=True
        return res

    def getNode(self,node):
        return self.graph[node.value]

    def setEnd(self,val):        
        self.end=self.graph[val]

    def setStart(self,val):
        self.start=self.graph[val]

    def reset(self):
        for node in self.nodes:
            node.visited=False
        
graph=Graph()
        
for actor in json['actors']:
    actor_name=actor['name']
    actor_movies=actor['movies']
    n = Node(actor_name)
    graph.addNode(n)
    for movie in actor_movies:
        m=Node(movie)
        if graph.isinGraph(m):
            m=graph.getNode(m)
        else:
            graph.addNode(m)
        n.addLinks(m)

# for node in graph.nodes:
#     print(node.value)
#     print('links:')
#     for link in node.links:
#         print(link.value)
#     print('__________')


graph.setEnd('Kevin Bacon')
graph.setStart('Kevin Bacon')


def bfs(graph,start,end):
    graph.reset()
    graph.setEnd(end)
    graph.setStart(start)
    queue=deque([])
    start = graph.start
    start.visited=True
    queue.append(start)

    while len(queue)>0:
        current=queue.popleft()
        if graph.end==current:
            found=current
            break
        for child in current.links:
            if not child.visited:
                child.visited=True
                child.parent=current
                queue.append(child)
    res=''
    trace=found
    while not trace==start:
        res+=trace.value+'<--'
        trace=trace.parent
    return res + trace.value

print(bfs(graph,'Jack Nicholson','Kevin Bacon'))
print(bfs(graph,'Leonard DiCaprio','Tom Hanks'))
