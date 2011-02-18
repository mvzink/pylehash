'''
Created on Feb 3, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

from twisted.internet.protocol import DatagramProtocol
from pylehash.telex import Telex
from pylehash import hash

class Switch(DatagramProtocol):
    '''
    TODO: Document the Switch class
    TODO: Add a repository of other Ends accessible by hash, IPPStr, IPPTuple, etc.
    '''
    def __init__(self):
        self.count = 0
        self.buckets = []
        self.handlers = []
        for i in range(0,161):
            self.buckets.append({})

    def datagramReceived(self, datagram, addr):
        '''
        Tells the quasi-global state object to handle the telex, passing along
        ourselves so things can be send
        '''
        self.handle(Telex(data=datagram), addr)

    def handle(self, telex, ipp):
        self.count += 1
        print "Received ", telex, "from", ipp[0], ":", ipp[1], "#", self.count
        self.send(Telex(other_dict={'+foo':'bar'}), ipp)

    def send(self, telex, ipp):
        '''
        Writes the given telex to the transport, sending it to the given IPP
        
        TODO: (Optionally?) modify telex to increase _br, _to, _line etc.
        '''
        self.transport.write(telex.dumps(), ipp)
    
    def complete_bootstrap(self, ipp):
        self.ipp = ipp

    def bucket_for(self, ipp):
        d = self.distance(ipp)
        return self.buckets[d]

    def distance(self, ipp):
        return hash.distance(self.ipp, ipp)

    def add_end(self, ipp):
        self.bucket_for(ipp)[hash.hexhash(ipp)] = ipp

