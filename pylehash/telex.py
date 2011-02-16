'''
Created on Feb 3, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>
'''

import pylehash #@UnresolvedImport @UnusedImport
import simplejson as json

class Telex(dict):
    '''
    TODO: Write docs for Telex
    '''

    def __init__(self, data=None, other_dict={}):
        self.update(other_dict)
        if data:
            # TODO: catch eventuality of non-object at top level
            self.update(json.loads(data))
    
    def to(self, to):
        if isinstance(to, tuple):
            self['_to'] = to[0] + ':' + str(to[1])
        if isinstance(to, str):
            self['_to'] = to
    
    def dumps(self):
        return json.dumps(self)
