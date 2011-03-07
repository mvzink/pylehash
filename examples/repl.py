'''
This is a REPL loop that gives the local var "switch" to be a pylehash switch.
Allows for some easy experimentation.

Created on Mar 6, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

from twisted.internet import stdio
from twisted.protocols import basic
import pylehash

class InteractWithSwitch(basic.LineReceiver):
    from os import linesep as delimiter

    def __init__(self, switch):
        self.state = {'sw': switch}
        self.lines = 0

    def connectionMade(self):
        self.transport.write('>>> ')

    def lineReceived(self, line):
        self.lines += 1
        try:
            src = compile(line, '<input %d>' % self.lines, 'single')
            eval(src, self.state)
        except:
            pass
        self.transport.write('>>> ')

def main():
    port, switch = pylehash.get_switch_from_args()
    stdio.StandardIO(InteractWithSwitch(switch))
    pylehash.reactor.listenUDP(port, switch)
    pylehash.reactor.run()

if __name__ == '__main__':
    main()
