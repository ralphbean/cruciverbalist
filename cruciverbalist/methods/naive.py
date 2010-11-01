
import itertools
import pprint

from core import BaseMethod

class NaiveMethod(BaseMethod):
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

        def form_it(p):
            for i in range(len(word_dict.keys())):
                word_dict._voltron[word_dict.keys()[i]] = {
                    'r' : p[i][0][0],
                    'c' : p[i][0][1],
                    'd' : p[i][1],
                }

            if word_dict.valid():
                count = word_dict.count_letters()
                if count not in scoreboard:
                    print "New one...", count
                    print word_dict 
                scoreboard[count] = scoreboard.get(count, 0) + 1

        for p in every_possible:
            form_it(p)

        print "Scoreboard is..."
        pprint.pprint(scoreboard)

        self._formed = True
        return word_dict

