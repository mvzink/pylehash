'''
Created on Feb 3, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

from twisted.internet.protocol import DatagramProtocol
from pylehash import hash, handlers, Telex

class Switch(DatagramProtocol):
    '''
    TODO: Document the Switch class
    '''
    def __init__(self, seed_ipp=('telehash.org', 42424)):
        self.ipp = None
        self.buckets = []
        self.handlers = {}
        self.add_handler(handlers.BootstrapHandler(seed_ipp))
        for i in range(0,161):
            self.buckets.append({})

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
            handler(telex, ipp, self)

    def send(self, telex=None, to=None):
        '''
        Writes the given telex to the transport, sending it to the given IPP
        
        TODO: (Optionally?) modify telex to increase _br, _to, _line etc.
        Also see question in switch.handle()'s docstring
        '''
        if telex and to:
            self.transport.write(telex.dumps(), to)

    def bucket_for(self, ipp):
        d = self.distance(ipp)
        return self.buckets[d]

    def distance(self, ipp):
		return hash.distance(self.ipp, ipp)

    def add_end(self, ipp):
        self.bucket_for(ipp)[hash.hexhash(ipp)] = ipp

    def add_handler(self, handler):
        self.handlers[id(handler)] = handler

    def remove_handler(self, handler):
        self.handlers.pop(id(handler))
