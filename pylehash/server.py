'''
Created on Feb 3, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

from pylehash import switch

def run(port=0):
    from protocol import Telehash
    from twisted.internet import reactor
    state = switch.Switch()
    reactor.listenUDP(port, Telehash(state))
    reactor.run()

if __name__ == '__main__':
    run(5555)
