'''
Created on Feb 3, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

from twisted.internet.protocol import DatagramProtocol
import hash, handlers
from .telex import Telex
from .end import End
from .util import ippstr

class Switch(DatagramProtocol):
    '''
    TODO: Document the Switch class
    '''
    def __init__(self, seed_ipp=None):
        self.ipp = None
        self.buckets = []
        self.handlers = {}
        self.seed_ipp = seed_ipp

        if self.seed_ipp:
            self.add_handler(handlers.BootstrapHandler(self.seed_ipp))
        else:
            for handler in handlers.default_handlers():
                self.add_handler(handler)

        for _ in range(0,161):
            self.buckets.append({})

    def startProtocol(self):
        '''
        Sends a useless telex to a seed in hopes of getting something back and
        learning our IPP. Only does so if we don't have an IPP but do have a
        seed to contact.
        '''
        if self.ipp == None and self.seed_ipp != None:
            t = Telex(other_dict={'+end':hash.hexhash('1.2.3.4:5555')})
            self.send(t, End(self.seed_ipp))

    def datagramReceived(self, datagram, addr):
        '''
        Called by the Twisted framework when a UDP packet arrives.
        
        Turns the datagram into a Telex and calles switch.handle on it with the
        address of the sender.
        '''
        self.handle(Telex(data=datagram), addr, len(datagram))

    def handle(self, telex, ipp, bytes):
        '''
        Runs the given telex and sender by all our current handlers.
        '''
        print "<<", ippstr(ipp), ":", telex.dumps()
        end = self.find_end(ipp)
        end.br += bytes
        for handler in self.handlers.values():
            handler(telex, end, self)

    def send(self, telex=None, to=None):
        '''
        Writes the given telex to the transport, sending it to the given IPP
        
        TODO: (Optionally?) modify telex to include _br, _to, _line etc.
        Also see question in NOTES.txt
        '''
        if telex and to:
            telex['_to'] = ippstr(to.ipp)
            telex['_br'] = to.br
            print ">>", ippstr(to.ipp), ":", telex.dumps()
            self.transport.write(telex.dumps(), to.ipp)

    def bucket_for(self, end):
        '''
        Returns the bucket associating ends the same distance from us as the
        given end (End or ippstr)
        '''
        d = self.distance(end)
        return self.buckets[d]

    def distance(self, end):
        '''
        Finds the distance between the given end (End or ippstr) and ourselves.
        '''
        return hash.distance(self.ipp, end)

    def add_end(self, end):
        '''
        Adds the given end to our buckets iff an end isn't already there.
        '''
        if not hash.hexhash(end) in self.bucket_for(end):
            self.bucket_for(end)[hash.hexhash(end)] = end

    def find_end(self, ipp):
        '''
        Tries to find the end for the given ipptup in our beckets. If it isn't
        there, it adds a new one.
        '''
        e = End(ipp)
        if self.ipp:
            if hash.hexhash(e) in self.bucket_for(e):
                return self.bucket_for(e)[hash.hexhash(e)]
            else:
                self.add_end(e)
                return e
        else:
            return e

    def add_handler(self, handler):
        self.handlers[id(handler)] = handler

    def remove_handler(self, handler):
        self.handlers.pop(id(handler))
