'''
Created on Feb 15, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

from .telex import Telex
from .util import ippstr, ipptup

def default_handlers():
    return [NewTapHandler(), EndHandler(), SeeHandler()]

class Handler(object):
    
    def __call__(self, telex, from_end, switch):
        if self.matches(telex, from_end, switch):
            self.handle(telex, from_end, switch)

    def handle(self, telex, from_end, switch):
        '''
        handler.handle(telex, from_end, switch) -> None
        
        Performs actions as appropriate based on the handler's own state and the
        given telex, ipp, and switch state.
        
        Should be overridden by subclasses.
        '''
        pass
    
    def matches(self, telex, from_end, switch):
        '''
        handler.matches(telex, from_end, switch) -> True|False
        
        Returns True or 
        '''

class TapHandler(Handler):

    def __init__(self, tests):
        self.tests = tests

    def handle(self, telex, from_end, switch):
        '''
        Should be overridden to actually handle the telex.
        '''
        pass

    def matches(self, telex, from_end, switch):
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
    
    def handle(self, telex, from_end, switch):
        '''
        TODO: Test this
        '''

        if '_hop' in telex:
            if telex['_hop'] > 4:
                return None
            else:
                telex['_hop'] += 1
        else:
            telex['_hop'] = 1

        switch.send(telex=telex, to=self.to)

class EndHandler(TapHandler):
    def __init__(self):
        super(EndHandler, self).__init__([{'has': ['+end']}])
    
    def handle(self, telex, from_end, switch):
        sees = map(lambda e: ippstr(e.ipp), switch.bucket_for(telex['+end']).values()[:3])
        sees = filter(lambda e: e != ippstr(from_end.ipp), sees)
        t = Telex(other_dict={'.see':sees})
        switch.send(telex=t, to=from_end)

class NewTapHandler(TapHandler):
    def __init__(self):
        super(NewTapHandler, self).__init__([{'has': ['.tap']}])

    def handle(self, telex, from_end, switch):
        new_handler = ForwardingTapHandler(telex['.tap'], from_end)
        switch.add_handler(new_handler)

class BootstrapHandler(Handler):
    def __init__(self, ipp):
        self.seed_ipp = ipp

    def matches(self, telex, from_end, switch):
        return switch.ipp == None and from_end.ipp == self.seed_ipp and '_to' in telex

    def handle(self, telex, from_end, switch):
        switch.ipp = ipptup(telex['_to'])
        for handler in default_handlers():
            switch.add_handler(handler)
        switch.remove_handler(self)

class SeeHandler(TapHandler):

    def __init__(self):
        super(SeeHandler, self).__init__([{'has': ['.see']}])

    def handle(self, telex, from_end, switch):
        switch.add_end(from_end)
