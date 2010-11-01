#!/usr/bin/env python

import itertools
import pprint

class InvalidPuzzleException(Exception):
    pass
class Puzzle(dict):
    def __init__(self, *args, **kwargs):
        self._formed = False
        self._voltron = {}
        self.F = '#'
        super(Puzzle, self).__init__(*args, **kwargs)

    def form_like_voltron(self):
        """ Using my key, value pairs, form a crossword puzzle

        Method must be a str and may be 'naive', 'hard' or 'genetic
        """
        self._voltron = {}
        n = len(self.keys())
        size = max(n * 2, max(map(lambda x : len(x), self.keys())))
        print "size is", size
        print "   n is", n

        perms = map(list, itertools.permutations(range(size), 2))
        idens = map(list, zip(range(size), range(size)))
        possibs = perms + idens
        print "possibs is", len(possibs)
        
        cartesian = list(itertools.product(possibs, ['across', 'down']))
        print "cartesi is", len(cartesian)
        print "   self is", len(self)
        every_possible = itertools.permutations(cartesian, r=len(self))

        print "testing them"
        scoreboard = {}
        for p in every_possible:
            for i in range(len(self.keys())):
                self._voltron[self.keys()[i]] = {
                    'r' : p[i][0][0],
                    'c' : p[i][0][1],
                    'd' : p[i][1],
                }

            if self.valid():
                count = self.count_letters()
                if count not in scoreboard:
                    print "New one...", count
                    print self
                scoreboard[count] = scoreboard.get(count, 0) + 1

        print len(every_possible), "total possible combos"
        print "Scoreboard is..."
        pprint.pprint(scoreboard)

        self._formed = True
   
    def count_letters(self):
        grid = self.build_grid()
        count = 0
        for row in grid:
            for ch in row:
                if ch != self.F:
                    count += 1
        return count

    def valid(self):
        try:
            grid = self.build_grid()
            # look for written-over words (subwords)
            for d in self._voltron.values():
                if d['d'] == 'across':
                    if d['c'] != 0 and \
                       grid[d['r']][d['c']-1] != self.F:
                        return False
                else:
                    if d['r'] != 0 and \
                       grid[d['r']-1][d['c']] != self.F:
                        return False

            # look for unintended words
            n = len(grid)
            for r, c, in [(r, c) for r in range(n) for c in range(n)]:
                if grid[r][c] == self.F:
                    continue

                # backtrack left
                _c = c
                while _c > 0 and grid[r][_c-1] != self.F:
                    _c -= 1

                if grid[r][_c] == self.F:
                    _c += 1

                # lookup the word, scan right and verify
                word = None
                for k in self._voltron.keys():
                    if not (self._voltron[k]['r'] == r and
                            self._voltron[k]['c'] == _c and
                            self._voltron[k]['d'] == 'across'):
                        continue
                    word = k
                
                if not word and grid[r][_c+1] != self.F:
                    return False
                
                if word:
                    for i in range(len(word)):
                        if grid[r][_c+i] == word[i]:
                            continue
                        return False

                    if (len(grid[r]) > _c + len(word) and
                        grid[r][_c+len(word)] != self.F):
                        return False

                # backtrack up
                _r = r
                while _r > 0 and grid[_r-1][c] != self.F:
                    _r -= 1

                if grid[_r][c] == self.F:
                    _r += 1

                # lookup the word, scan down and verify
                word = None
                for k in self._voltron.keys():
                    if not (self._voltron[k]['r'] == _r and
                            self._voltron[k]['c'] == c and
                            self._voltron[k]['d'] == 'down'):
                        continue
                    word = k

                if not word and grid[_r+1][c] != self.F:
                    return False

                if word:
                    for i in range(len(word)):
                        if grid[_r+i][c] == word[i]:
                            continue
                        return False

                    if (len(grid[_r]) > r + len(word) and
                        grid[_r+len(word)][c] != self.F):
                        return False

                
                
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
        grid = [[self.F for j in range(size)] for i in range(size)]
        for word, config in self._voltron.iteritems():
            for i in range(len(word)):
                if config['d'] == 'across':
                    if grid[config['r']][config['c'] + i] != self.F and\
                       grid[config['r']][config['c'] + i] != word[i]:
                        raise InvalidPuzzleException
                    grid[config['r']][config['c'] + i] = word[i]
                elif config['d'] == 'down':
                    if grid[config['r'] + i][config['c']] != self.F and\
                       grid[config['r'] + i][config['c']] != word[i]:
                        raise InvalidPuzzleException
                    grid[config['r'] + i ][config['c']] = word[i]
                else:
                    raise KeyError, "Illegal value in voltron config"
        return grid

if __name__ == '__main__':
    words = ['trotsky', 'bakunin', 'lenin', 'marx']
    d = dict([(w, '') for w in words])
    p = Puzzle(d)
    p.form_like_voltron()

