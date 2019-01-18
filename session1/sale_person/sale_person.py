import numpy as np
import itertools
import names
import sys
from matplotlib import pyplot as plt

number_of_cities=int(sys.argv[1])
n_o_b=30
cities=[]

class City:
    def __init__(self,x,y,name):
        self.name=name
        self.x=x
        self.y=y

for i in range(number_of_cities):
    x=np.random.random()*100
    y=np.random.random()*100
    city=City(x,y,names.get_first_name())
    cities.append(city)

def fact(n):
    res=1
    for i in range(2,n+1):
        res*=i
    return res

def swap(array,i,j):
    temp=array[i]
    array[i]=array[j]
    array[j]=temp
    return array

def reverse_from(index,array):
    temp_array=[]
    for i in range(index,len(array)):
        temp_array.append(array.pop())
    for el in temp_array:
        array.append(el)
    return array

def trad_to_array(index_list,array):
    res=[]
    for i in index_list:
        res.append(array[i])
    return res

def get_largeY(array,index):
    ret_index=-1
    ret=0
    for i in range(len(array)):
        if array[index]<array[i]:
            ret=i
            if ret > ret_index:
                ret_index=ret
    return ret_index

def get_largeX(array):
    ret_index=-1
    for i in range(len(array)-1):
        if array[i]<array[i+1] and i > ret_index:
            ret_index=i
    if ret_index==-1:
        return None
    else:
        return ret_index

def each_possibility(array):
    load=0
    shuff_arrays=[]
    shuff_arrays.append(array)
    indexlist=list(range(len(array)))
    undred=fact(number_of_cities)
    print('Construction a list of each possibility')
    while True:
        load+=1
        percent=load/undred
        print(int(percent*n_o_b)*'*'+(n_o_b-int(percent*n_o_b))*'-'+'  '+str(round(percent*100,3))+'%', end="\r")
        X=get_largeX(indexlist)
        if X==None:
            return shuff_arrays
        Y=get_largeY(indexlist,X)
        indexlist=swap(indexlist,X,Y)
        indexlist=reverse_from(X+1,indexlist)
        temp_array=trad_to_array(indexlist,array)
        shuff_arrays.append(temp_array)

def dist_between(city1,city2):
    x_tmp=abs(city1.x-city2.x)
    y_tmp=abs(city1.y-city2.y)
    return np.sqrt(pow(x_tmp,2)+pow(y_tmp,2))

def search_for_the_best_path(cities):
    best_dist=float('inf')
    best_shuffl= []
    e_pos=each_possibility(cities)
    undred=len(e_pos)
    count=0
    print('Searching for the best path')
    print(' ')
    for shuff_cities in e_pos:
        percent=round(count/undred*n_o_b)
        print('Searching : '+percent*'*'+(n_o_b-percent)*'-', end="\r")
        count+=1
        tot_dist=0
        for i in range(len(shuff_cities)-1):
            tot_dist+=dist_between(shuff_cities[i],shuff_cities[i+1])
        if tot_dist < best_dist:
            best_shuffl=shuff_cities
            best_dist=tot_dist
    print('Completed!                                              ')
    return best_dist,best_shuffl

def print_result(dist,cities):
    traj=''
    print('')
    print('Best dist is around '+str(int(round(dist)))+'km')
    for city in cities:
        traj+=city.name+'-->'
    print(traj[:-3])


data=search_for_the_best_path(cities)

fig=plt.figure()
ax = plt.axes(xlim=(0, 200), ylim=(0, 100))
plt.xticks([]), plt.yticks([])

line, = ax.plot([], [], marker="o",lw=2,color="green")

x=[]
y=[]
for city in data[1]:
    x.append(city.x)
    y.append(city.y)
line.set_data(x, y)
plt.show()

