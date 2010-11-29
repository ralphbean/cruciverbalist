
import itertools
import pprint

from core import BaseMethod
from naive import form_it


class HeuristicMethod(BaseMethod):
    def good_guess(self, dct, working_p=[]):
        """ Recursive """
        if len(dct.keys()) == len(working_p):
            return [working_p]
        else:
            possibs = []
            # try placing it on its own across (naive)
            # try placing it anywhere it will fit across
            # try placing it anywhere it will fit down
            
            # try placing it on its own across (naive)
            if len(working_p) == 0:
                ri, ci = [dct.grid_center()]*2
                entries = [[(ri, ci), 'across'], [(ri, ci), 'down']]
                for entry in entries:
                    possibs.extend( self.good_guess(dct, working_p + [entry]) )
                return possibs

            word = dct.keys()[len(working_p)]
            r = working_p[-1][0][0]
            c = working_p[-1][0][1]
            c += len(word) + 1
            entry = [(r, c), 'across']
            possibs.extend( self.good_guess(dct, working_p + [entry]) )

            # Look through all the already placed words.
            for i in range(len(working_p)):
                # for every placed that `word` fits, try it
                for j in range(len(dct.keys()[i])):
                    for k in range(len(word)):
                        if dct.keys()[i][j] == word[k]:
                            print dct.keys()[i][j], "matches", word[k]
                            print " for", dct.keys()[i], "and", word
                            ri, ci = working_p[i][0]
                            entry = []
                            if working_p[i][1] == 'down':
                                entry = [ (ri + j, ci - k), 'across']
                            else:
                                entry = [ (ri - k, ci + j), 'down']
                            possibs.extend( 
                                self.good_guess(dct, working_p + [entry]) )

            return possibs


    def produce(self, word_dict):
        """ Using my key, value pairs, form a crossword puzzle

        Method must be a str and may be 'naive', 'hard' or 'genetic
        """
        
        possibilities = self.good_guess(word_dict)
        for p in possibilities:
            print p
            dct = form_it(p, word_dict)
            print dct
        sys.exit(0)

        for p in possibilities:
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

