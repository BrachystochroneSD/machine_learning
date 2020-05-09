#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "city.h" // for city struct
#include <time.h>

/* Set const :
   -width and height of the terrain
   -the number of cities
   -population number per period
   -the mutation rate
   -the power of the best score*/

const unsigned int MAX_ITERATION=1000;
const int WIDTH=100;
const int HEIGHT=100;
const int NUM_CITIES=70;
const int POP_NUMBER=1000;
const double MUT_RATE=15;
const int POW_SCORE=50;

FILE *file;
double *fitness;
double *score;

void random_shuffle(city*, size_t);
void evaluate_fitness(city**);
size_t bestScore(void);
void cross_and_mut(city**);

int main(void){

  /* time_t t; */
  /* srand((unsigned) time(&t)); */

  fitness=malloc(POP_NUMBER*sizeof(double));
  score=malloc(POP_NUMBER*sizeof(double));
  //set a list of cities with random position
  city CITIES[NUM_CITIES];

  for( int i=0; i < NUM_CITIES; i++ ){
    city tmp={(float)rand()/RAND_MAX*WIDTH,(float)rand()/RAND_MAX*HEIGHT};
    CITIES[i]=tmp;
  }

  // create a population of randomly shuffled cities
  city **population=malloc(POP_NUMBER*sizeof(city*));
  for (size_t i=0;i<POP_NUMBER;i++){
    city *new_cities=malloc(NUM_CITIES*sizeof(city));
    for (size_t j = 0; j < NUM_CITIES; j++){
      new_cities[j]=CITIES[j];
    }
    random_shuffle(new_cities,NUM_CITIES);
    population[i]=new_cities;
  }

  evaluate_fitness(population); //evaluate_fitness of this pop

  file=fopen("/home/samrenfou/Dropbox/machine_learning/session2/cversion/gnuplot/data.txt","w");

  for(size_t i=0; i<MAX_ITERATION;i++){
    cross_and_mut(population);
    evaluate_fitness(population);
    size_t bestindex=bestScore();
    printf("The best path for now is %.0fkm long\n",score[bestindex]);

    for( size_t j=0; j< NUM_CITIES; j++){
      fprintf(file, "%f %f\n",population[bestindex][j].x,population[bestindex][j].y);
    }
    fprintf(file,"\n");
    fprintf(file,"\n");
  }
  fclose(file);

  // free all the shits
  free(fitness);
  free(score);
  for (size_t i=0;i<POP_NUMBER;i++){
    free(population[i]);
  }
  free(population);
}

void random_shuffle(city *city_list, size_t n){
  //Shuffle an city_list of cities
  if (n > 1){
    for (size_t i = 0; i < n - 1; i++){
      size_t j = (i + rand())%n;
      city t = city_list [j];
      city_list[j] = city_list[i];
      city_list[i] = t;
    }
  }
}

double get_tot_dist(city *city_list) {
  /* Return the total distance of */
  /* a path between cities stored in city Array */
  double result = 0;
  for( size_t i=0; i<NUM_CITIES-1; i++ ){
    double tmpx = fabs(city_list[i].x - city_list[i+1].x);
    double tmpy = fabs(city_list[i].y - city_list[i+1].y);
    result += sqrt(pow(tmpx,2)+pow(tmpy,2));
  }
  return result;
}

void evaluate_fitness(city **pop){
  /* evaluate the fitness of all the
     randomized list of cities and
     store them in an array "fitness"*/

  double sum_score=0;

  for (size_t i=0; i<POP_NUMBER; i++){
    score[i]=get_tot_dist(pop[i]);
    sum_score += 1/pow(score[i],POW_SCORE);
  }
  for (size_t i=0; i<POP_NUMBER; i++){
    fitness[i]=1/pow(score[i],POW_SCORE)/sum_score;
  }
}

size_t bestScore(void){
  double best_fit=0;
  size_t best_index;
  for(size_t i=0;i<POP_NUMBER;i++){
    if (fitness[i]>best_fit){
      best_fit=fitness[i];
      best_index=i;
    }
  }
  return best_index;
}

size_t pick(void){
  /* return fitness-based-randomly picked index of a population
   */
  size_t index=0;
  double selector = (double)rand()/(double)RAND_MAX;
  while(selector > 0){
    selector-=fitness[index];
    index+=1;
  }
  return index - 1;
}

city pop_city(city* list_cities, size_t n){
  /* pop last city on the array list_cities
     and return the poped city
     should never be call if n = 1 in the code for now
     but can be a problem in the future */
  size_t new_size=NUM_CITIES-n;
  city res=list_cities[new_size];
  list_cities=realloc(list_cities, sizeof(city)*new_size);
  return res;
}

void remove_city(city c, city* list_cities, size_t n){
  /* remove city on the array list_cities
     return the modified array pointer*/
  size_t new_size = NUM_CITIES-n;
  if (new_size>0){
    double cx=c.x;
    double cy=c.y;
    size_t j=0;
    for(size_t i=0; i<new_size+1; i++){
      double testx=list_cities[i].x;
      double testy=list_cities[i].y;
      if(testx==cx && testy==cy){
	j++;
      }
      list_cities[i]=list_cities[j];
      j++;
    }
  }
  list_cities=realloc(list_cities, sizeof(city)*new_size);
}

city *copy_cities(city *cities){
  city *copied_cities= malloc(sizeof(city)*NUM_CITIES);
  for(size_t i=0; i < NUM_CITIES; i++){
    copied_cities[i]=cities[i];
  }
  return copied_cities;
}

city *crossover(city* cities1,city* cities2){
  city *child_cities=malloc(sizeof(city)*NUM_CITIES);

  city *copy_cities1=copy_cities(cities1);
  city *copy_cities2=copy_cities(cities2);

  city ind1; // \individus chosen
  city ind2; // /
  unsigned int choic=0; // permit to choose periodically between copy_cities1 and 2
  for(size_t i=0; i<NUM_CITIES-1; i+=2){
    if (choic == 0){
      // prend la première paire de copy_cities1 et l'ajoute à child
      ind1=pop_city(copy_cities1,i+1);
      ind2=pop_city(copy_cities1,i+2);
      // supprime la paire dans copy_cities2
      remove_city(ind1,copy_cities2,i+1);
      remove_city(ind2,copy_cities2,i+2);
      // put the pair in the child
      child_cities[i]=ind2;
      child_cities[i+1]=ind1;
      choic=1;
    } else {
      // prend la première paire de copy_cities2 et l'ajoute à child
      ind1=pop_city(copy_cities2,i+1);
      ind2=pop_city(copy_cities2,i+2);
      // supprime la paire dans copy_cities1
      remove_city(ind1,copy_cities1,i+1);
      remove_city(ind2,copy_cities1,i+2);
      // put the pair in the child
      child_cities[i]=ind2;
      child_cities[i+1]=ind1;
      choic=0;
    }
  }
  if (NUM_CITIES%2 == 1){
    city last_one=pop_city(copy_cities1,NUM_CITIES);
    remove_city(last_one,copy_cities2,NUM_CITIES);
    child_cities[NUM_CITIES-1]=last_one;
  }
  return child_cities;
}

void mutate(city *cities){
  /* Randomly (based on MUT_RATE) mutate a list of
     cities byswaping two random city */
  double dice_roll=(double)rand()/(double)RAND_MAX;
  if(dice_roll<=MUT_RATE/100){
    size_t i=rand()%NUM_CITIES;
    size_t j=rand()%NUM_CITIES;
    city tmp=cities[i];
    cities[i]=cities[j];
    cities[j]=tmp;
  }
}

void cross_and_mut(city **pop){
  /* pick two pseudo-randomly(fitness based) two member
     of the previous population, crossover them, mutate them randomly
     and fill the next generation with them */

  city **temp_pop=malloc(POP_NUMBER*sizeof(city*));
  for(size_t i=0; i<POP_NUMBER;i++){
    size_t i1 = pick();
    size_t i2 = pick(); // and andré

    city *child_cities=crossover(pop[i1],pop[i2]);
    mutate(child_cities);
    temp_pop[i]=child_cities;
  }
  for(size_t i; i<POP_NUMBER;i++){
    // replace the old population
    free(pop[i]);
    pop[i]=temp_pop[i];
  }
  free(temp_pop); // don't need the temp_pop
}
