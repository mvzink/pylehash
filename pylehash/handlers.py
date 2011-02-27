'''
Created on Feb 15, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

from pylehash import ippstr, ipptup, Telex

class Handler(object):
    
    def __call__(self, telex, from_ipp, switch):
        if self.matches(telex, from_ipp, switch):
            self.handle(telex, from_ipp, switch)

    def handle(self, telex, from_ipp, switch):
        '''
        handler.handle(telex, from_ipp, switch) -> None
        
        Performs actions as appropriate based on the handler's own state and the
        given telex, ipp, and switch state.
        
        Should be overridden by subclasses.
        '''
        pass
    
    def matches(self, telex, from_ipp, switch):
        '''
        handler.matches(telex, from_ipp, switch) -> True|False
        
        Returns True or 
        '''

class TapHandler(Handler):

    def __init__(self, tests):
        self.tests = tests

    def handle(self, telex, from_ipp, switch):
        '''
        Should be overridden to actually handle the telex.
        '''
        pass

    def matches(self, telex, from_ipp, switch):
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
    
    def handle(self, telex, from_ipp, switch):
        '''
        TODO: Test this
        '''
        switch.send(telex=telex, to=self.to)

class EndHandler(TapHandler):
    def __init__(self):
        super(EndHandler, self).__init__([{'has': ['+end']}])
    
    def handle(self, telex, from_ipp, switch):
        sees = map(ippstr, switch.bucket_for(telex['+end']).values()[:3])
        t = Telex(other_dict={'.see':sees})
        switch.send(telex=t, to=from_ipp)

class NewTapHandler(TapHandler):
    def __init__(self):
        super(NewTapHandler, self).__init__([{'has': ['.tap']}])

    def handle(self, telex, from_ipp, switch):
        new_handler = ForwardingTapHandler(telex['.tap'], from_ipp)
        switch.add_handler(new_handler)

class BootstrapHandler(Handler):
    def __init__(self, ipp):
        self.seed_ipp = ipp

    def matches(self, telex, from_ipp, switch):
        return switch.ipp == None and from_ipp == self.seed_ipp and '_to' in telex

    def handle(self, telex, from_ipp, switch):
        switch.ipp = ipptup(telex['_to'])
        for handler in default_handlers():
            switch.add_handler(handler)
        switch.remove_handler(self)

def default_handlers():
    return [NewTapHandler(), EndHandler()]
