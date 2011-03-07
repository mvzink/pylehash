'''
Created on Feb 27, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

import copy
import hash

class End(object):
    def __init__(self, ipp):
        self.ipp = ipp
        self.bytes_received = 0

class EndManager(object):

    def __init__(self, switch):
        self.switch = switch
        self._buckets = {}

    def bucket(self, i):
        if i not in self._buckets:
            self._buckets[i] = {}
        return self._buckets[i]

    def bucket_for(self, end):
        '''
        Returns the bucket associating ends the same distance from us as the
        given end (End or ippstr)
        '''
        return self.bucket(self.distance(end))

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

    def near(self, end_ipp_or_hash):
        b = self.bucket_for(end_ipp_or_hash).values()
        if len(b) < 3:
            d = self.distance(end_ipp_or_hash)
            for i in reversed(range(1, d)):
                b += self.bucket(i).values()
                if len(b) >= 3:
                    b = b[:3]
                    break
        return b
