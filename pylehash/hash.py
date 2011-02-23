'''
Created on Feb 3, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

from hashlib import sha1
from math import floor, log

def hexhash(ipp):
    if isinstance(ipp, str):
        return sha1(ipp).hexdigest()
    elif isinstance(ipp, tuple):
        return hexhash(ipp[0] + ':' + str(ipp[1]))

def hexbin(hex):
    return int(hex, 16)

def binhash(ipp):
    return hexbin(hexhash(ipp))
    
def distance(hash1, hash2):
    if isinstance(hash1, tuple):
        a = binhash(hash1)
    else:
        a = hexbin(hash1)

    if isinstance(hash2, tuple):
        b = binhash(hash2)
    else:
        b = hexbin(hash2)

    diff = a ^ b
    if diff == 0:
        return diff
    else:
        return int(160 - floor(log(diff, 2)))
