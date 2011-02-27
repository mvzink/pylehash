#!/usr/bin/env python
'''
Created on Feb 3, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

from pylehash import Switch
from twisted.internet import reactor

def run(port, switch):
    reactor.listenUDP(port, switch)
    reactor.run()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Start a pylehash server')
    parser.add_argument('port', nargs='?', type=int, default=0,
        help='The port number to listen on (default: random)')
    parser.add_argument('--seed', nargs=2, dest='seed', metavar=('HOST', 'PORT'), default=['208.68.163.247', '42424'],
        help='The port and host of a seed to contact. \
            (default: 208.68.163.247:42424 aka telehash.org:42424)')
    parser.add_argument('--no-seed', nargs=2, dest='no_seed', metavar=('HOST', 'PORT'), default=False,
        help='Don\'t contact a seed; usually means we will be a seed for a network. \
            Overrides --seed (default: no)')
    args = parser.parse_args()

    if args.no_seed:
        s = Switch()
        s.ipp = (args.no_seed[0], int(args.no_seed[1]))
    elif args.seed:
        s = Switch(seed_ipp=(args.seed[0], int(args.seed[1])))

    run(args.port, s)
