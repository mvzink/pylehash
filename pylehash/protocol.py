'''
Created on Feb 3, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

from twisted.internet.protocol import DatagramProtocol
from pylehash.telex import Telex

class Telehash(DatagramProtocol):
    
    def __init__(self, switch):
        self.switch = switch
    
    def datagramReceived(self, datagram, addr):
        '''
        Tells the quasi-global state object to handle the telex, then writes
        back the response if any
        '''
        msg = self.switch.handle(Telex(data=datagram), addr)
        if msg: self.transport.write(msg.dumps(), addr)
