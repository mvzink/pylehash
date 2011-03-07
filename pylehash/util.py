'''
Created on Feb 27, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

def ippstr(ipp):
    '''
    Converts an IPP tuple to an IPP string
    ippstr(('1.2.3.4', 5678)) == '1.2.3.4:5678'
    '''
    return ipp[0] + ':' + str(ipp[1])

def ipptup(ipp):
    '''
    Converts an IPP string to an IPP tuple
    ipptup('1.2.3.4:5678') == ('1.2.3.4', 5678)
    '''
    ip, p = ipp.split(':')
    return (ip, int(p))
