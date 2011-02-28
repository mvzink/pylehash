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
        self.handle(Telex(data=datagram), addr)

    def handle(self, telex, ipp):
        '''
        Runs the given telex and sender by all our current handlers.
        '''
        print "Received ", telex, "from", ipp[0], ":", ipp[1]
        for handler in self.handlers.values():
            handler(telex, End(ipp), self)

    def send(self, telex=None, to=None):
        '''
        Writes the given telex to the transport, sending it to the given IPP
        
        TODO: (Optionally?) modify telex to include _br, _to, _line etc.
        Also see question in NOTES.txt
        '''
        if telex and to:
            telex['_to'] = ippstr(to.ipp)
            self.transport.write(telex.dumps(), to.ipp)

    def bucket_for(self, end):
        d = self.distance(end)
        return self.buckets[d]

    def distance(self, end):
        if isinstance(end, End):
            return hash.distance(self.ipp, end.ipp)
        elif isinstance(end, str):
            return hash.distance(hash.hexhash(self.ipp), end)

    def add_end(self, end):
        self.bucket_for(end)[hash.hexhash(end)] = end

    def add_handler(self, handler):
        self.handlers[id(handler)] = handler

    def remove_handler(self, handler):
        self.handlers.pop(id(handler))
