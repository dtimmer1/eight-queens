import numpy as np
import eight_queens.position as pos
from random import randint, random, choice

POP_SIZE = 500  # the higher the population size, the fewer generations needed but more computation time for each
MUT_RATE = .05  # must be between 0 and 1


def first_pop():
    # initializes the first generation, populating it with individuals
    population = []
    for x in range(POP_SIZE):
        indi = pos.Position()
        indi.place_queens()
        indi.set_fitness()
        population.append(indi)
    return population


def get_fitness(position):
    return position.fitness


def sort_and_cut(pop):
    # sorts a population by fitness, then removes the lowest fitness half
    pop.sort(key=lambda e: e.fitness)
    new_size = int(POP_SIZE/2)
    half_pop = pop[new_size:]
    return half_pop


def recombine_mutate(ind1, ind2):
    # combines queens of ind1 and ind2 into ret_ind, then randomly mutates
    ret_ind = pos.Position()
    for i in range(len(ind1.queens)):
        if randint(0, 1) == 0:
            ret_ind.queens[i] = (ind1.queens[i])
        else:
            ret_ind.queens[i] = (ind2.queens[i])
    for q in ret_ind.queens:
        for i in range(len(q)):
            if random() < MUT_RATE:
                q[i] = randint(0, pos.NUM_QUEENS-1)
    repeat = True
    while repeat:
        # eliminates duplicate queens
        check = True
        for i in range(len(ret_ind.queens)):
            for j in range(i + 1, len(ret_ind.queens)):
                if np.array_equal(ret_ind.queens[i], ret_ind.queens[j]):
                    ret_ind.queens[i] = np.array([randint(0, pos.NUM_QUEENS-1), randint(0, pos.NUM_QUEENS-1)])
                    check = False
        if check:
            repeat = False
    ret_ind.queens = ret_ind.queens[np.argsort(ret_ind.queens[:, 0])]
    ret_ind.set_fitness()
    return ret_ind


def repopulate(pop):
    # adds in half of population by randomly selecting individuals weighted by fitness,
    # then recombines and mutates by calling the method above
    weighted_list = []
    for indi in pop:
        for i in range(indi.fitness):
            weighted_list.append(indi)
    while len(pop) < POP_SIZE:
        pop.append(recombine_mutate(choice(weighted_list), choice(weighted_list)))


def main():
    # runs everything
    found = False
    count = 0
    pop = first_pop()
    while not found:
        pop = sort_and_cut(pop)
        repopulate(pop)
        count+= 1
        for p in pop:
            if p.fitness == (pos.FITNESS_TABLE[pos.NUM_QUEENS])**2:
                found = True
    pop.sort(key=lambda e: e.fitness, reverse=True)
    pop[0].render()
    print("Needed generations: " + str(count))


main()