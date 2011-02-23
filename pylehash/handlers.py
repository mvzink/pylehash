'''
Created on Feb 15, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

from pylehash.hash import *

class TapHandler(object):

    def __init__(self, tests):
        self.tests = tests

    def handle(self, telex, switch):
        '''
        Should be overridden to actually handle the telex.
        '''
        pass

    def matches(self, telex):
        telex_matches = None

        # We test each case independently
        for test in self.tests:
            test_matches = True
            
            # We test each clause dependent upon the previous ones
            for clause in test:
                if clause == 'has':
                    for key in test[clause]:
                        # Both this clause and the previous clauses
                        # must match for the test to match
                        print(key in telex)
                        test_matches = test_matches and key in telex
                elif clause == 'is':
                    for key in test[clause]:
                        test_matches = test_matches and telex[key] == test[clause][key]
                # We need all the clauses to match, so break if this one doesn't
                if (test_matches == False):
                    break

            # We only need one test to match, so break if this one does            
            if test_matches == True:
                telex_matches = True
                break
            # If this one doesn't match, we will still test the successive ones, but
            # in case this is the last one we say the telex doesn't match
            elif test_matches == False:
                telex_matches = False
            
        return telex_matches

class ForwardingTapHandler(TapHandler):
    def __init__(self, tests, to):
        super(ForwardingTapHandler, self).__init__(tests)
        self.to = to
    
    def handle(self, telex, switch):
        switch.send(telex, self.to)
