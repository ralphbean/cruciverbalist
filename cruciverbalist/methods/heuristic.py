
import itertools
import pprint

from core import BaseMethod
from naive import form_it


class HeuristicMethod(BaseMethod):
    def produce(self, word_dict):
        """ Using my key, value pairs, form a crossword puzzle

        Method must be a str and may be 'naive', 'hard' or 'genetic
        """
        
        n = len(word_dict.keys())
        size = max(n * 2, max(map(lambda x : len(x), word_dict.keys())))
        print "size is", size
        print "   n is", n

        perms = map(list, itertools.permutations(range(size), 2))
        idens = map(list, zip(range(size), range(size)))
        possibs = perms + idens
        print "possibs is", len(possibs)

        cartesian = list(itertools.product(possibs, ['across', 'down']))
        print "cartesi is", len(cartesian)
        print "w_dict  is", len(word_dict)
        every_possible = itertools.permutations(cartesian, r=len(word_dict))

        print "testing them"
        scoreboard = {}

        for p in every_possible:
            dct = form_it(p, word_dict)
            if dct and dct.count_letters() not in scoreboard:
                print "New one...", dct.count_letters()
                print word_dict 
            if dct:
                scoreboard[dct.count_letters()] = \
                        scoreboard.get(dct.count_letters(), 0) + 1

        print "Scoreboard is..."
        pprint.pprint(scoreboard)

        self._formed = True
        return word_dict

