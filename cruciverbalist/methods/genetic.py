
import itertools
import pprint
import sys
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
            return d.count_letters() + d.squared_size()
        else:
            return 10000

    def select(self, pop):
        ind = [randint(0, len(pop)-1) for i in range(2)]
        return [pop[i] for i in ind]

    def introduce(self, pop, chi1, chi2):
        r1 = r2 = randint(len(pop)/2, len(pop)-1)
        while r2 == r1:
            r2 = randint(len(pop)/2, len(pop)-1)
        pop[r1] = chi1
        pop[r2] = chi2
        return pop

    def mutate(self, org):
        # TODO -- more operators:
            # move whole blocks
            # rotate whole blocks
            # line up word?
        def random_mut(org):
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
        def move_block(org):
            i1 = i2 = randint(0, len(org)-2)
            while i2 == i1:
                i2 = randint(0, len(org)-2)
            if i2 < i1:
                tmp = i2
                i2 = i1
                i1 = tmp

            choice = randint(0, 3)
            for i in range(i1, i2+1):
                if choice == 0:
                    org[i][0][0] = org[i][0][0] - 1
                elif choice == 1:
                    org[i][0][0] = org[i][0][0] + 1
                elif choice == 2:
                    org[i][0][1] = org[i][0][1] - 1
                elif choice == 3:
                    org[i][0][1] = org[i][0][1] + 1
                else:
                    raise ValueError, "WTF"
            return org
        def move_connected(org):
            return org
        def rotate_block(org):
            return org
        def rotate_connected(org):
            return org
        def line_up_word(org):
            return org
        def line_up_connected(org):
            return org
        methods = {
            'random mutate' : random_mut,
            'move block' : move_block,
            #'move connected block' : move_connected,
            #'rotate block' : rotate_block,
            #'rotate connected block' : rotate_connected,
            #'line up word' : line_up_word,
            #'line up connected block' : line_up_connected,
        }
        mutation_rate = 0.05
        if random() < mutation_rate:
            method_i = randint(0, len(methods.keys())-1)
            org = methods[methods.keys()[method_i]](org)
        return org

        return org

    def crossover(self, org1, org2):
        pt = randint(0, len(org1)-2)
        return (
            org1[:pt] + org2[pt:-1] + [None],
            org2[:pt] + org1[pt:-1] + [None],
        )

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

        generations = 100000
        pop_size = 100
        population = [
            [random_spec() for j in range(n)]+[None] for i in range(pop_size)]

        population = [self.evaluated(org) for org in population]
        population.sort(lambda x, y : cmp(x[-1], y[-1]))
        print "Initial population:"
        pprint.pprint(population)

        best_score = population[0][-1]
        print "Best score:", best_score
        for gen in range(generations):
            if population[0][-1] < best_score:
                best_score = population[0][-1]
                print
                print "New best score", best_score, "at gen", gen
                winner = form_it(population[0][:-1], word_dict)
                print "Winner is:"
                print winner
                print

            if gen % 100 == 0:
                avg = sum([org[-1] for org in population]) / float(len(population))
                print "\r     ", gen, "Avg score", avg,
                sys.stdout.flush()

            org1, org2 = self.select(population)
            chi1, chi2 = self.crossover(org1, org2)
            chi1 = self.evaluated(self.mutate(chi1))
            chi2 = self.evaluated(self.mutate(chi2))
            population = self.introduce(population, chi1, chi2)
            population.sort(lambda x, y : cmp(x[-1], y[-1]))
            #print "Population after generation", gen
            #pprint.pprint(population)

        winner = form_it(population[0][:-1], word_dict)
        print "Winner is:"
        pprint.pprint(winner)

        return winner

