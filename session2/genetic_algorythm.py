import random
import sys

char_list=list(" AZERTYUIOPQSDFGHJKLMWXCVBNazertyuiopqsdfghjklmwxcvbn,.!?;:+=éèà")
len_char_list=len(char_list)


def random_string(lengh):
    res=''
    for i in range(lengh):
        random_letter=char_list[random.randint(0,len_char_list-1)]
        res+=random_letter
    return res

class ADN:
    def __init__(self,string):
        self.list_string=list(string)
        self.score=0
        self.fitness=0

    def __str__(self):
        res=''
        for i in self.list_string:
            res+=str(i)
        return res

    def mutate(self,mut_rate):
        for i in range(len(self.list_string)):
            if random.random() <= mut_rate/100:
                self.list_string[i]=char_list[random.randint(0,len_char_list-1)]

class Population:

    def __init__(self,desired_string,N,mut_rate):
        self.des_string=list(desired_string)
        self.N=N
        self.mut_rate=mut_rate
        self.pop=[]

        for i in range(N):
            ind=ADN(random_string(len(desired_string)))
            self.pop.append(ind)

    def evaluate_fitness(self):
        sum_score=0
        for ind in self.pop:
            score_count=0
            for i in range(len(ind.list_string)):
                if ind.list_string[i]==self.des_string[i]:
                    score_count+=1
            ind.score=pow(score_count,3)
            sum_score+=ind.score
        for ind in self.pop:
            ind.fitness=ind.score/sum_score

    def pick(self):
        index=0
        selector=random.random()
        while selector>0 and index < len(self.pop)-1:
            selector-=self.pop[index].fitness
            index+=1
        index-=1
        return self.pop[index]

    def crossover(self,ADN1,ADN2):
        cross_ind=random.randint(0,len(self.des_string)-1)
        child_string=''
        for i in range(0,cross_ind):
            child_string+=str(ADN1.list_string[i])
        for i in range(cross_ind,len(self.des_string)):
            child_string+=str(ADN2.list_string[i])
        return child_string

    def next_gen(self):
        new_pop=[]
        for i in range(self.N):
            parent1=self.pick()
            parent2=self.pick()
            child=ADN(self.crossover(parent1,parent2))
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

def genetic_algorythm(population):
    gen_count=0
    while True:
        gen_count+=1
        population.evaluate_fitness()
        population.next_gen()
        print(' Search: '+str(population.evaluate()),end="\r")
        if population.evaluate().list_string == population.des_string:
            print('Found after '+str(gen_count)+' generations')
            break


phrase=sys.argv[1]
pop=Population(phrase,100,1)

genetic_algorythm(pop)
