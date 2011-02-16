from test_stuff import TestCase, selfipp, closeipp, faripp
from pylehash import hash

class TestHash(TestCase):
    
    def test_hexhash_arbitrary_string(self):
        test_hash = 'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3'
        assert hash.hexhash('test') == test_hash
        
    def test_hexhash_ipp_str(self):
        ipp_hash = 'bc117be99339576519af05e91d51376feabd4706'
        assert hash.hexhash('127.0.0.1:5555') == ipp_hash
        
    def test_hexhash_ipp_tuple(self):
        ipp_hash = 'bc117be99339576519af05e91d51376feabd4706'
        assert hash.hexhash(('127.0.0.1',5555)) == ipp_hash

    def test_hexbin_short(self):
        assert hash.hexbin('e') == 14
        assert hash.hexbin('abc123abc123') == 188846015496483

    def test_hexbin_long(self):
        hexval = 'bc117be99339576519af05e91d51376feabd4706'
        longval = 1073680171875912199119184443246291065335917135622L
        assert hash.hexbin(hexval) == longval

    def test_binhash_arbitrary_string(self):
        longval = 1073680171875912199119184443246291065335917135622L
        assert hash.binhash('127.0.0.1:5555') == longval

    def test_distance_to_self_is_zero(self):
        assert hash.distance(selfipp, selfipp) == 0

    def test_distance_is_commutative(self):
        assert hash.distance(selfipp, faripp) == hash.distance(faripp, selfipp)

    def test_distance_correct_for_faripp(self):
        assert hash.distance(selfipp, faripp) == 17

    def test_distance_correct_for_closeipp(self):
        assert hash.distance(selfipp, closeipp) == 1

    def test_distance_is_an_int(self):
        assert isinstance(hash.distance(selfipp, closeipp), int)


from pylehash.switch import Switch

class TestSwitch(TestCase):

    def setUp(self):
        self.s = Switch()
        self.s.complete_bootstrap(selfipp)

    def test_switch_complete_bootstrap(self):
        assert self.s.ipp == selfipp
        
    def test_switch_add_end_adds_end(self):
        self.s.add_end(closeipp)
        assert self.s.bucket_for(closeipp)[hash.hexhash(closeipp)]

        
    def test_switch_bucket_for_gives_correct_bucket(self):
        self.s.add_end(closeipp)
        o = self.s.bucket_for(closeipp)
        assert self.s.buckets.index(o) == hash.distance(selfipp, closeipp)
        self.s.add_end(faripp)
        p = self.s.bucket_for(faripp)
        assert self.s.buckets.index(p) == hash.distance(selfipp, faripp)


from pylehash.telex import Telex

class TestTelex(TestCase):

    def test_telex_acts_like_a_dictionary(self):
        t = Telex()
        t['+test'] = 'testing'
        assert t['+test'] == 'testing'

    def test_telex_constructor_takes_optional_json_data(self):
        t = Telex(data='{"+test": "testing"}')
        assert t['+test'] == 'testing'

    def test_telex_constructor_takes_optional_other_dictionary(self):
        t = Telex(other_dict={'+test':'testing'})
        assert t['+test'] == 'testing'

    def test_telex_dumps_to_json(self):
        t = Telex()
        t['+test'] = 'testing'
        print(t.dumps())
        assert t.dumps() == '{"+test": "testing"}'

from pylehash.default_handlers import TapHandler

class TestTapHandler(TestCase):
    '''
    More than anything, this should serve as an example of how to write
    a handler class that conforms to the accepted protocol.
    See pylehash.default_handlers for TapHandler.
    '''

    def setUp(self):
        '''
        Defines a tap handler that should match any telex which either
            1. has both +foo and +bar signals, or
            2. has a +foo signal equal to "no_bar"
        '''
        self.t = TapHandler([
            {'has': ['+foo', '+bar']},
            {'is': {'+foo': 'no_bar'}}
        ])
        self.match_has = Telex(other_dict={
            '+foo': 'a_bar',
            '+bar': 'still_a_bar'
        })
        self.match_is = Telex(other_dict={
            '+foo': 'no_bar'
        })
        self.match_both = Telex(other_dict={
            '+foo': 'no_bar',
            '+bar': 'except_still_a_bar'
        })
        self.no_match = Telex(other_dict={
            '+foo': 'where_is_the_bar'
        })

    def test_tap_handler_correctly_tests_for_matching_telexes(self):
        assert self.t.matches(self.match_has)
        assert self.t.matches(self.match_is)
        assert self.t.matches(self.match_both)
        assert not self.t.matches(self.no_match)

