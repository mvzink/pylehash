'''
Created on Feb 3, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

def ippstr(ipp):
    return ipp[0] + ':' + str(ipp[1])


from telex import Telex
from switch import Switch
import hash
import handlers
