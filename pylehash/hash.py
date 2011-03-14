'''
Created on Feb 3, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

from hashlib import sha1
from math import floor, log
from .util import ippstr
from .end import End

def hexhash(end):
    if isinstance(end, End):
        return hexhash(end.ipp)
    elif isinstance(end, tuple):
        return hexhash(ippstr(end))
    elif isinstance(end, str):
        return sha1(end).hexdigest()

def hexbin(hex):
    return int(hex, 16)

def binhash(end):
    return hexbin(hexhash(end))
    
def distance(hash1, hash2):
    if isinstance(hash1, tuple):
        a = binhash(hash1)
    elif isinstance(hash1, End):
        a = binhash(hash1.ipp)
    else: # is hash
        a = hexbin(hash1)

    if isinstance(hash2, tuple):
        b = binhash(hash2)
    elif isinstance(hash2, End):
        b = binhash(hash2.ipp)
    else: # is hash
        b = hexbin(hash2)

    diff = a ^ b
    if diff == 0:
        return diff
    else:
        return int(160 - floor(log(diff, 2)))
