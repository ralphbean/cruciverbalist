#!/usr/bin/env python

from methods import NaiveMethod
from methods import GeneticMethod
from methods import HeuristicMethod

class InvalidPuzzleException(Exception):
        pass

class Puzzle(dict):
    def __init__(self, method=NaiveMethod(), **kwargs):
        self._formed = False
        self._voltron = {}
        self.F = '#'

        print "Working with words:", kwargs.keys()
        super(Puzzle, self).__init__(**kwargs)
        print type(method)
        self = method.produce(self)

    def bounds(self):
        grid = self.build_grid()
        maxR, maxC, minR, minC = 0, 0, 1000000, 1000000
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                ch = grid[r][c]
                if ch != self.F:
                    if r > maxR:
                        maxR = r
                    if c > maxC:
                        maxC = c
                    if r < minR:
                        minR = r
                    if c < minC:
                        minC = c
        return maxR, minR, maxC, minC 

    def squared_size(self):
        maxR, minR, maxC, minC = self.bounds()
        return max([maxR-minR, maxC-minC])

    def count_letters(self):
        grid = self.build_grid()
        count = 0
        for row in grid:
            for ch in row:
                if ch != self.F:
                    count += 1
        return count

    def score(self):
        return self.count_letters() + self.squared_size()

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
                
                # make sure i'm isolated if I'm isolated
                if not word and grid[r][_c+1] != self.F:
                    return False
                
                if word:
                    # otherwise.. scan right and verify
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

                # make sure i'm isolated if I'm isolated
                if not word and grid[_r+1][c] != self.F:
                    return False

                if word:
                    # otherwise.. scan down and verify
                    for i in range(len(word)):
                        if grid[_r+i][c] == word[i]:
                            continue
                        return False

                    if (len(grid[_r]) > r + len(word) and
                        grid[_r+len(word)][c] != self.F):
                        return False
        except IndexError:
            return False
        except InvalidPuzzleException:
            return False
        return True

    def __str__(self):
        # Otherwise...
        grid = self.build_grid()
        res = ''
        maxR, minR, maxC, minC = self.bounds()
        for r in range(minR-1, maxR+2):
            for c in range(minC-1, maxC+2):
                res += grid[r][c]
            res += '\n'
        return res


    def grid_center(self):
        return self.grid_size() / 2

    def grid_size(self):
        n = len(self.keys())
        return max(n * 2, max(map(lambda x : len(x), self.keys()))) * 2 * 2

    def build_grid(self):
        size = self.grid_size()
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
    _words = [
        'dog',
        'dietpepsi', 'rr', 'ido', 'ti', 'eve', 'step', 'ja', 'janet', 'bigboi',
        'serena', 'scoutt', 'toni', 'dr', 'orb']
    for i in range(1, len(_words)):
        words = _words[:i]
        d = dict([(w, '') for w in words])
        p = Puzzle(method=HeuristicMethod(), **d)
        print "Done"
        print p

