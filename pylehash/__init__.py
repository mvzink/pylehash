'''
Created on Feb 3, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

from twisted.internet import reactor
from .util import ippstr, ipptup
from .telex import Telex
from .switch import Switch
from .end import End, EndManager
import hash
import handlers


def make_switch(port, ip=None, seed=None):
    if ip:
        s = Switch(ipp = (ip[0], port))
    elif seed:
        s = Switch(seed_ipp=(seed[0], int(seed[1])))
    else:
        s = Switch(seed_ipp=('208.68.163.247', 42424))
    return s

def run_switch(port, switch):
    from . import reactor
    reactor.listenUDP(port, switch)
    reactor.run()

def get_switch_from_args():
    import argparse
    parser = argparse.ArgumentParser(description='Start a pylehash server')
    parser.add_argument('port', nargs='?', type=int, default=0,
        help='The port number to listen on (default: random)')
    parser.add_argument('--seed', nargs=2, dest='seed', metavar=('HOST', 'PORT'), default=False,
        help='The port and host of a seed to contact. \
            (default: 208.68.163.247:42424 aka telehash.org:42424)')
    parser.add_argument('--no-seed', nargs=1, dest='ip', metavar='HOST', default=False,
        help='Don\'t contact a seed; usually means we will be a seed for a network. Argument specifies our own IP address. \
            Overrides --seed (default: no)')
    args = parser.parse_args()

    return (args.port, make_switch(args.port, seed=args.seed, ip=args.ip))
