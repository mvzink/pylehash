'''
Created on Feb 3, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

from twisted.internet.protocol import DatagramProtocol
import hash, handlers
from .telex import Telex
from .end import End, EndManager
from .util import ippstr

class Switch(DatagramProtocol):
    '''
    TODO: Document the Switch class
    '''
    def __init__(self, ipp=False, seed_ipp=False):
        self.ipp = ipp
        self.seed_ipp = seed_ipp
        self.ends = EndManager(self)
        self.handlers = {}

        if self.ipp:
            for handler in handlers.default_handlers():
                self.add_handler(handler)
        elif self.seed_ipp:
            self.add_handler(handlers.BootstrapHandler(self.seed_ipp))

    def startProtocol(self):
        '''
        Sends a useless telex to a seed in hopes of getting something back and
        learning our IPP. Only does so if we don't have an IPP but do have a
        seed to contact.
        '''
        if self.seed_ipp and not self.ipp:
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
        end = self.ends.find(ipp)
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

    def add_handler(self, handler):
        self.handlers[id(handler)] = handler

    def remove_handler(self, handler):
        self.handlers.pop(id(handler))
