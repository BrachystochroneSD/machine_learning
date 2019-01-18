import numpy
import random

class Node:
    def __init__(self, val):
        self.v=val
        self.ln=None
        self.rn=None

    def addNode(self,node):
        if self.v > node.v:
            if self.ln == None:
                self.ln = node
            else:
                self.ln.addNode(node)
        elif self.v < node.v:
            if self.rn == None:
                self.rn = node
            else:
                self.rn.addNode(node)

    def check(self):
        if self.ln != None:
            self.ln.check()
        print(self.v)
        if self.rn != None:
            self.rn.check()

    def uncheck(self):
        if self.rn != None:
            self.rn.uncheck()
        print(self.v)
        if self.ln != None:
            self.ln.uncheck()

class Tree:
    def __init__(self):
        self.root=None
        
    def addValue(self,val):
        newnode=Node(val)
        if self.root==None:
            self.root=newnode
        else:
            self.root.addNode(newnode)

    def printsorted(self):
        self.root.check()
    def printreversesorted(self):
        self.root.uncheck()

        
tree=Tree()

for i in range(10):
    tree.addValue(random.randint(0,100000))

