'''
Created on Feb 27, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

def ippstr(ipp):
    return ipp[0] + ':' + str(ipp[1])

def ipptup(ipp):
    ip, p = ipp.split(':')
    return (ip, int(p))
