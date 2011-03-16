'''
A simple bulletin-posting/receiving app.

Start it up, and use commands like so:

    +<board>        to subscribe to the board "board"
    <board>: <msg>  to send "msg" to "board"

Remember that the 20 byte hash of the board name, the message, and the other
TeleHash load must fit within 1400 bytes. The packet will be dropped otherwise.

Also, uses... just the worst, stupidest algorithms ever. I'll make it better one
day, along with actual iterative node finding.

Created on Mar 15, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

from twisted.internet import stdio
from twisted.protocols import basic
import pylehash

class BulletinAppUI(basic.LineReceiver):
    from os import linesep as delimiter

    def __init__(self, switch):
        self.switch = switch

    def connectionMade(self):
        self.transport.write('Starting up! Use "+<board>" to subscribe and "<board>: <msg>" to post!\n')

    def lineReceived(self, line):
        try:
            cmd, sep, msg = line.strip().partition(' ')
            if cmd[0] == '+':
                self.subscribe(cmd[1:])
            elif len(msg) is not 0 and cmd[-1] == ':':
                self.post(cmd[:-1], msg)
            else:
                self.transport.write("I'm sorry?")
        except Exception as e:
            print e

    def do_subscribe_taps(self, board):
        h = pylehash.hash.hexhash(board)
        t = pylehash.Telex(other_dict={'.tap': [
                {'is': {'+board': h}}
            ]})
        for s in self.switch.ends.near(h):
            self.switch.send(telex=t, to=s)

    def subscribe(self, board):
        h = pylehash.hash.hexhash(board)
        t = pylehash.Telex(other_dict={'+end': h})
        for s in self.switch.ends.near(h):
            self.switch.send(telex=t, to=s)
        pylehash.reactor.callLater(2.0, self.do_subscribe_taps, board)

    def post(self, board, msg):
        h = pylehash.hash.hexhash(board)
        t = pylehash.Telex(other_dict={'+board': h, '+msg': msg})
        for s in self.switch.ends.near(h):
            self.switch.send(telex=t, to=s)

def main():
    port, switch = pylehash.get_switch_from_args()
    stdio.StandardIO(BulletinAppUI(switch))
    pylehash.reactor.listenUDP(port, switch)
    pylehash.reactor.run()

if __name__ == '__main__':
    main()
