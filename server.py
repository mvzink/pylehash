'''
Created on Feb 3, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

def run(port=0):
    from pylehash import Switch
    from twisted.internet import reactor
    s = Switch(seed_ipp=('127.0.0.1', 6666))
    reactor.listenUDP(port, s)
    reactor.run()

if __name__ == '__main__':
    run(5555)
