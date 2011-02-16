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
    diff = binhash(hash1) ^ binhash(hash2)
    if diff == 0:
        return diff
    else:
        return int(160 - floor(log(diff, 2)))

def ipp_distance(ipp1, ipp2):
    return hash_distance(binhash(ipp1), binhash(ipp2))
