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
        self.startup_callbacks = []
        self.bootstrap_completed_callbacks = []

        if self.ipp:
            for handler in handlers.default_handlers():
                self.add_handler(handler)
        elif self.seed_ipp:
            self.add_handler(handlers.BootstrapHandler(self.seed_ipp))
            self.add_startup_callback(send_bootstrap_telex)

    def startProtocol(self):
        '''
        Sends a useless telex to a seed in hopes of getting something back and
        learning our IPP. Only does so if we don't have an IPP but do have a
        seed to contact.
        '''
        for callback in self.startup_callbacks:
            callback(self)

    def complete_bootstrap(self, ipp):
        self.ipp = ipp
        for callback in self.bootstrap_completed_callbacks:
            callback(self)

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

    '''
    TODO: (Possibly) handle callbacks in the same way as handlers (with ids)
    '''
    def add_startup_callback(self, callback):
        self.startup_callbacks.append(callback)

    def add_bootstrap_completed_callback(self, callback):
        self.bootstrap_completed_callbacks.append(callback)

def send_bootstrap_telex(switch):
    '''
    Sends an arbitrary bootstrap telex. Should be relocated, I believe.
    '''
    t = Telex(other_dict={'+end':hash.hexhash('1.2.3.4:5555')})
    switch.send(t, switch.ends.find(switch.seed_ipp))
