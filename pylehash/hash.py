'''
Created on Feb 3, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

from hashlib import sha1

def hexhash(ipp):
    if isinstance(ipp, str):
        return sha1(ipp).hexdigest()
    elif isinstance(ipp, tuple):
        return hexhash(ipp[0] + ':' + str(ipp[1]))

def hexbin(hex):
    return int(hex, 16)

def binhash(ipp):
    return hexbin(hexhash(ipp))