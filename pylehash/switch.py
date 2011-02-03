'''
Created on Feb 3, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

from pylehash.telex import Telex #@UnresolvedImport

class Switch(object):
    '''
    TODO: Document the Switch class
    TODO: Add a repository of other Ends accessible by hash, IPPStr, IPPTuple, etc.
    '''
    def __init__(self):
        self.count = 0

    def handle(self, telex, ipp):
        self.count += 1
        print "Received ", telex, "from", ipp[0], ":", ipp[1], "#", self.count
        return Telex(to=ipp, other_dict={'+foo':'bar'})