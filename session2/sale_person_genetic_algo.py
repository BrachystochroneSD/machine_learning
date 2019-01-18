import numpy as np
import random
import names
import copy
import sys
import time
from matplotlib import pyplot as plt
from matplotlib import animation

if len(sys.argv) < 4:
    print('---------------------------------')
    print('Need to get the parameters in the form of: ')
    print('number_of_cities(int) population_number_per_generation(int) mutation_rate(float, in percent) power_scoring(int)')
    print('For example: python this_script.py 15 100 80 2')
    print('---------------------------------')    
    sys.exit()
else:
    num_cities=int(sys.argv[1])
    pop_number=int(sys.argv[2])
    mutation_rate=float(sys.argv[3])
    pow_score=int(sys.argv[4])


# Initialize random cities with random names

cities=[]
class City:
    def __init__(self,x,y,name):
        self.name=name
        self.x=x
        self.y=y

for i in range(num_cities):
    x=random.random()*100
    y=random.random()*100
    city=City(x,y,names.get_first_name())
    cities.append(city)

def dist_between(city1,city2):
    x_tmp=abs(city1.x-city2.x)
    y_tmp=abs(city1.y-city2.y)
    return np.sqrt(pow(x_tmp,2)+pow(y_tmp,2))

def crossover(ADN1,ADN2):
    cur_parrent=copy.copy(ADN1.list_cities),copy.copy(ADN2.list_cities)
    curr=0
    child=[]
    while len(child)<num_cities:
        if len(cur_parrent[curr])==1:
            child.append(cur_parrent[(curr+1)%2].pop(0))
            return ADN(child)
        i_ind=cur_parrent[curr].pop(0)
        j_ind=cur_parrent[curr].pop(0)
        child.append(i_ind)
        child.append(j_ind)
        cur_parrent[(curr+1)%2].remove(i_ind)
        cur_parrent[(curr+1)%2].remove(j_ind)
        curr=(curr+1)%2
    return ADN(child)

def get_tot_dist(cities_list):
    tot_dist=0
    for i in range(len(cities_list)-1):
        tot_dist+=dist_between(cities_list[i],cities_list[i+1])
    return tot_dist

def random_shuffle(array):
    res=[]
    l=len(array)
    while len(res)!=l:
        res.append(array.pop(random.randint(0,len(array)-1)))
    return res

class ADN:
    def __init__(self,cities):
        self.list_cities=cities
        self.fitness=0
        self.score=0
        self.count=0

    def __str__(self):
        res=''
        for city in self.list_cities:
            res+=str(city.name)+'-->'
        return res[:-3]

    def mutate(self,mut_rate):
        if random.random() <= mut_rate/100:
            i= random.randint(0,len(self.list_cities)-1)
            j= random.randint(0,len(self.list_cities)-1)
            temp=self.list_cities[i]
            self.list_cities[i]=self.list_cities[j]
            self.list_cities[j]=temp

class Population:

    def __init__(self,N,mut_rate,popopow):
        self.N=N
        self.mut_rate=mut_rate
        self.pop=[]
        self.popopow=popopow

        for i in range(N):
            ind=ADN(random_shuffle(copy.copy(cities)))
            self.pop.append(ind)
        self.evaluate_fitness()

    def evaluate_fitness(self):
        sum_score=0
        for ind in self.pop:
            ind.score=get_tot_dist(ind.list_cities)
            sum_score+=1/pow(ind.score,self.popopow)
        for ind in self.pop:
            ind.fitness=1/pow(ind.score,self.popopow)/sum_score

    def pick(self):
        index=0
        selector=random.random()
        while selector > 0:
            selector-=self.pop[index].fitness
            index+=1
        index-=1
        return self.pop[index]

    def next_gen(self):
        new_pop=[]
        for i in range(self.N):
            parent1=self.pick()
            parent2=self.pick()
            child=crossover(parent1,parent2)
            child.mutate(self.mut_rate)
            new_pop.append(child)
        self.pop=new_pop

    def evaluate(self):
        best_fit=0
        best_ind=self.pop[0]
        for ind in self.pop:
            if ind.fitness > best_fit:
                best_fit= ind.fitness
                best_ind=ind
        return best_ind

    def overall_score(self):
        sum_score=0
        for ind in self.pop:
            sum_score+=ind.score
        return sum_score/pop_number

    def __call__(self):
        #make the next_generation and return the best ind of the new gen
        self.next_gen()
        self.evaluate_fitness()
        return self.evaluate(),self.overall_score()

# Genetic algorythm 
pop=Population(pop_number,mutation_rate,pow_score)


# print the infos
fig=plt.figure(1)
ax = plt.axes(xlim=(0, 200), ylim=(0, 100))
plt.xticks([]), plt.yticks([])

line, = ax.plot([], [], marker="o",lw=2,color="green")
line2, = ax.plot([], [], marker="o", lw=2,color="red")

def frames():
    best_dist=float('inf')
    best_path=None
    gen=1
    while True:
        best_ind=pop()[0]
        best_score=best_ind.score
        oa_score=pop()[1]
        if (best_ind.score) < best_dist:
            best_dist=best_ind.score
            best_path=best_ind
        # print(best_score)
        gen+=1
        yield best_ind,best_path,oa_score,gen

def animate(args):
    x=[]
    y=[]
    x2=[]
    y2=[]
    for city in args[0].list_cities:
        x.append(city.x)
        y.append(city.y)
    for city in args[1].list_cities:
        x2.append(city.x+100)
        y2.append(city.y)
    line.set_data(x, y)
    line2.set_data(x2, y2)
    fig.suptitle('Current best (green): '+str(int(args[0].score))+'\n    Best of all (red): '+str(int(args[1].score)))
    return line,line2

anim = animation.FuncAnimation(fig, animate, frames=frames, interval=1)

# fig2=plt.figure(2)


# x=[]
# y=[]
# y2=[]

# def animate2(args):
#     x.append(args[3])
#     y.append(args[2])
#     y2.append(args[0].score)
#     plt.plot(x, y, color='g')
#     plt.plot(x, y2, color='orange')

# anim2 = animation.FuncAnimation(fig2, animate2, frames=frames, interval=1)


plt.show()
