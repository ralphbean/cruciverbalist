
import itertools
import pprint
from random import randint, random

from core import BaseMethod

def form_it(p, word_dict):
    for i in range(len(word_dict.keys())):
        word_dict._voltron[word_dict.keys()[i]] = {
            'r' : p[i][0][0],
            'c' : p[i][0][1],
            'd' : p[i][1],
        }

    if word_dict.valid():
        return word_dict
    else:
        return None
        
class GeneticMethod(BaseMethod):

    def evaluated(self, org):
        return org[:-1] + [self.fitness(org[:-1])]

    def fitness(self, org):
        d = form_it(org, self.word_dict)
        if d and d.valid():
            return d.count_letters()
        else:
            return 10000

    def select(self, pop):
        return pop[:2]
    def introduce(self, pop, chi1, chi2):
        pop = pop[:-2]
        pop.extend([chi1, chi2])
        return pop

    def mutate(self, org):
        mutation_rate = 0.3
        if random() < mutation_rate:
            print "MUTATING"
            i = randint(0, len(org)-2)
            j = randint(0,2)
            if j == 0:
                org[i] = ([randint(0, self.size), org[i][0][1]], org[i][1])
            elif j == 1:
                org[i] = ([org[i][0][0], randint(0, self.size)], org[i][1])
            else:
                if org[i][1] == 'down':
                    org[i] = (org[i][0], 'across')
                else:
                    org[i] = (org[i][0], 'down')
        return org

    def crossover(self, org1, org2):
        return org1, org2
        

    def produce(self, word_dict):
        """ Using my key, value pairs, form a crossword puzzle

        Method must be a str and may be 'naive', 'hard' or 'genetic
        """
        self.word_dict = word_dict
        
        n = len(word_dict.keys())
        size = max(n * 2, max(map(lambda x : len(x), word_dict.keys())))
        self.size = size
        print "size is", size
        print "   n is", n

        def random_spec():
            def rand_dir():
                return ['down', 'across'][randint(0,1)]
            return ([randint(0, size), randint(0, size)], rand_dir())

        generations = 100
        pop_size = 6
        population = [
            [random_spec() for j in range(n)]+[None] for i in range(pop_size)]

        population = [self.evaluated(org) for org in population]
        population.sort(lambda x, y : cmp(x[-1], y[-1]))
        print "Initial population:"
        pprint.pprint(population)

        for gen in range(generations):
            org1, org2 = self.select(population)
            chi1, chi2 = self.crossover(org1, org2)
            chi1 = self.mutate(chi1)
            chi2 = self.mutate(chi2)
            population = self.introduce(population, chi1, chi2)
            population.sort(lambda x, y : cmp(x[-1], y[-1]))
            print "Population after generation", gen
            pprint.pprint(population)

        winner = form_it(population[0][:-1], word_dict)

        print "Winner is:"
        pprint.pprint(winner)

        return winner

