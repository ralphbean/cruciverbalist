#!/usr/bin/env python

import itertools
import pprint

class InvalidPuzzleException(Exception):
    pass
class Puzzle(dict):
    def __init__(self, *args, **kwargs):
        self._formed = False
        self._voltron = {}
        super(Puzzle, self).__init__(*args, **kwargs)

    def form_like_voltron(self):
        """ Using my key, value pairs, form a crossword puzzle

        Method must be a str and may be 'naive', 'hard' or 'genetic
        """
        self._voltron = {}
        n = len(self.keys())
        size = max(n * 2, max(map(lambda x : len(x), self.keys())))

        perms = map(list, itertools.permutations(range(size), 2))
        idens = map(list, zip(range(size), range(size)))
        possibs = perms + idens
        
        cartesian = list(itertools.product(possibs, ['across', 'down']))
        #every_possible = list(itertools.product(cartesian, cartesian))
        every_possible = list(itertools.combinations(cartesian, r=2))

        print len(every_possible)
        for p in every_possible:
            for i in range(len(self.keys())):
                self._voltron[self.keys()[i]] = {
                    'r' : p[i][0][0],
                    'c' : p[i][0][1],
                    'd' : p[i][1],
                }

            if self.valid():
                print self
            else:
                print "Skipping.. invalid"

        self._formed = True
    
    def valid(self):
        try:
            grid = self.build_grid()
            # TODO -- look for unintended words
        except InvalidPuzzleException:
            return False
        return True

    def __str__(self):
        # Otherwise...
        grid = self.build_grid()
        res = ''
        # TODO -- trim grid down as far as we can
        for row in grid:
            for ch in row:
                res += ch
            res += '\n'
        return res


    def build_grid(self):
        n = len(self.keys())
        size = max(n * 2, max(map(lambda x : len(x), self.keys()))) * 2
        F = '#'
        grid = [[F for j in range(size)] for i in range(size)]
        for word, config in self._voltron.iteritems():
            for i in range(len(word)):
                if config['d'] == 'across':
                    if grid[config['r']][config['c'] + i] != F:
                        raise InvalidPuzzleException
                    grid[config['r']][config['c'] + i] = word[i]
                elif config['d'] == 'down':
                    if grid[config['r'] + i][config['c']] != F:
                        raise InvalidPuzzleException
                    grid[config['r'] + i ][config['c']] = word[i]
                else:
                    raise KeyError, "Illegal value in voltron config"
        return grid

if __name__ == '__main__':
    p = Puzzle({'ad':'', 'ab': "foo"})
    p.form_like_voltron()

