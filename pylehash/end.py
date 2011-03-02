'''
Created on Feb 27, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

import hash

class End(object):
    def __init__(self, ipp):
        self.ipp = ipp
        self.br = 0

class EndManager(object):

    def __init__(self, switch):
        self.switch = switch
        self._buckets = {}

    def bucket_for(self, end):
        '''
        Returns the bucket associating ends the same distance from us as the
        given end (End or ippstr)
        '''
        d = self.distance(end)
        if d not in self._buckets:
            self._buckets[d] = {}
        return self._buckets[d]

    def distance(self, end):
        '''
        Finds the distance between the given end (End or ippstr) and ourselves.
        '''
        return hash.distance(self.switch.ipp, end)        

    def add(self, end):
        '''
        Adds the given end to our buckets iff an end isn't already there.
        '''
        if not hash.hexhash(end) in self.bucket_for(end):
            self.bucket_for(end)[hash.hexhash(end)] = end

    def find(self, ipp):
        '''
        Tries to find the end for the given ipptup in our beckets. If it isn't
        there, it adds a new one.
        '''
        e = End(ipp)
        if self.switch.ipp:
            if hash.hexhash(e) in self.bucket_for(e):
                return self.bucket_for(e)[hash.hexhash(e)]
            else:
                self.add(e)
                return e
        else:
            return e
