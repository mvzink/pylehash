'''
Created on Feb 3, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

def run(port=0):
    from pylehash.switch import Switch
    from twisted.internet import reactor
    reactor.listenUDP(port, Switch())
    reactor.run()

if __name__ == '__main__':
    run(5555)
