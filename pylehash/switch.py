'''
Created on Feb 3, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

from pylehash.telex import Telex
import hash

class Switch(object):
    '''
    TODO: Document the Switch class
    TODO: Add a repository of other Ends accessible by hash, IPPStr, IPPTuple, etc.
    '''
    def __init__(self):
        self.count = 0
        self.buckets = []
        for i in range(0,161):
            self.buckets.append({})

    def handle(self, telex, ipp):
        self.count += 1
        line = self.line(ipp)
        print "Received ", telex, "from", ipp[0], ":", ipp[1], "#", self.count
        return Telex(to=ipp, other_dict={'+foo':'bar'})

    def complete_bootstrap(self, ipp):
        self.ipp = ipp

    def bucket_for(self, ipp):
        d = self.distance(ipp)
        return self.buckets[d]

    def distance(self, ipp):
        return hash.distance(self.ipp, ipp)

    def add_end(self, ipp):
        self.bucket_for(ipp)[hash.hexhash(ipp)] = ipp