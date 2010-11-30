
import itertools
import pprint
import sys

import shelve
PREFIX = "/tmp"

from core import BaseMethod

def unordered_form_it(p, word_dict):
    for i in range(len(p)):
        word_dict._voltron[p[i][2]] = {
            'r' : p[i][0][0],
            'c' : p[i][0][1],
            'd' : p[i][1],
        }

    if word_dict.valid():
        return word_dict
    else:
        return None

class HeuristicMethod(BaseMethod):
    def unchosen_words(self, dct, working_p):
        return [k for k in dct.keys() if k not in [ele[2] for ele in working_p]]

    def good_guess(self, dct, working_p=[], depth=0):
        """ Recursive """
        if len(dct.keys()) == len(working_p):
            return [working_p]

        # Sanity check for converting to unordered heuristic
        if len(working_p) > 0:
            for p in working_p:
                if not len(p) >= 3:
                    raise ValueError, "Invalid p len %i %s" % (len(p), str(p))

        possibs = []
        # try placing it on its own across (naive)
        # try placing it anywhere it will fit across
        # try placing it anywhere it will fit down
        
        if len(working_p) == 0:
            # Top of the tree....
            for word in self.unchosen_words(dct, working_p):
                print "Top of tree.  Starting with word '%s'" % word
                ri, ci = [dct.grid_center()]*2
                entry = [(ri,ci),'across',word,[]]
                subtree = self.good_guess(dct,working_p+[entry],depth+1)
                possibs.extend(subtree)
                print "    Subtree of size:  %i" % len(subtree)
                filename = "%s/%s-%s.possibs.dat" % (PREFIX,  self.id, word)
                print "    Writing subtree to %s" % filename
                d = shelve.open(filename)
                d['data'] = subtree
                d.close()
                print "    Done."
            return possibs

        for word in self.unchosen_words(dct, working_p):
            r = working_p[-1][0][0]
            c = working_p[-1][0][1]
            c += (len(working_p[-1][2]) + 1) * 2
            entry = [(r, c), 'across', word, []]
            possibs.extend( self.good_guess(dct, working_p + [entry], depth+1) )

            # Look through all the already placed words.
            for i in range(len(working_p)):
                # for every placed that `word` fits, try it
                for j in range(len(working_p[i][2])):
                    for k in range(len(word)):
                        if ( working_p[i][2][j] == word[k] and
                             not j in working_p[i][3] ):
                            ri, ci = working_p[i][0]
                            entry = []
                            if working_p[i][1] == 'down':
                                entry = [ (ri + j, ci - k), 'across', word, [k]]
                            else:
                                entry = [ (ri - k, ci + j), 'down', word, [k]]
                            possibs.extend(
                                self.good_guess(
                                    dct, working_p[:i]+[
                                        [
                                            working_p[i][0],
                                            working_p[i][1],
                                            working_p[i][2],
                                            working_p[i][3] + [j]
                                        ]
                                    ]+working_p[i+1:] + [entry], depth+1))
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
            d = unordered_form_it(p, word_dict)
            if d:
                if d.score() < best_score:
                    best = p
                    best_score = d.score()
        print 
        print "    Done measuring."
        if not best:
            print "BEST WAS NEVER SET... weird"
            raise ValueError, "WTF"
        return unordered_form_it(best, word_dict)


