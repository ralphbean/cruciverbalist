
import itertools
import pprint
import sys

from core import BaseMethod
from naive import form_it


class HeuristicMethod(BaseMethod):
    def good_guess(self, dct, working_p=[], depth=0):
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
                    possibs.extend(
                        self.good_guess(dct, working_p + [entry], depth+1) )
                return possibs

            word = dct.keys()[len(working_p)]
            r = working_p[-1][0][0]
            c = working_p[-1][0][1]
            c += (len(dct.keys()[len(working_p)-1]) + 1) * 2
            entry = [(r, c), 'across']
            possibs.extend( self.good_guess(dct, working_p + [entry], depth+1) )

            # Look through all the already placed words.
            for i in range(len(working_p)):
                # for every placed that `word` fits, try it
                for j in range(len(dct.keys()[i])):
                    for k in range(len(word)):
                        if dct.keys()[i][j] == word[k]:
                            ri, ci = working_p[i][0]
                            entry = []
                            if working_p[i][1] == 'down':
                                entry = [ (ri + j, ci - k), 'across']
                            else:
                                entry = [ (ri - k, ci + j), 'down']
                            possibs.extend( 
                                self.good_guess(dct, working_p + [entry], depth+1) )
            return possibs


    def produce(self, word_dict):
        """ Using my key, value pairs, form a crossword puzzle

        Method must be a str and may be 'naive', 'hard' or 'genetic
        """
       
        print "Developing a number of guesses..."
        possibs = self.good_guess(word_dict)
        print "    Done guessing.  %i reasonable possibilities." % len(possibs)
        best_score = 100000
        best = None
        print "Measuring the 'goodness' of each guess..."
        for i in range(len(possibs)):
            if i % 100 == 0:
                prog = (float(i)/len(possibs))
                print "\r    %%%.1f" % (100 * prog),
                bar_len = 65
                print "[", "=" * int(prog*bar_len),
                print " " * int((1-prog)*bar_len), "]",
                sys.stdout.flush()
            p = possibs[i]
            d = form_it(p, word_dict)
            if d:
                if d.score() < best_score:
                    best = p
                    best_score = d.score()
        print 
        print "    Done measuring."
        if not best:
            print "BEST WAS NEVER SET... weird"
            raise ValueError, "WTF"
        return form_it(best, word_dict)


