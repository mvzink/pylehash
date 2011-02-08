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



from pylehash.switch import Switch

class TestSwitch(TestCase):

    def setUp(self):
        self.s = Switch()
        self.s.complete_bootstrap(selfipp)

    def test_switch_complete_bootstrap(self):
        assert self.s.ipp == selfipp

    def test_switch_bucket_for_gives_correct_bucket(self):
        o = {'foo': 'bar'}
        self.s.buckets[1] = o
        assert o == self.s.bucket_for(closeipp)

    def test_switch_add_end_adds_end(self):
        self.s.add_end(closeipp)
        assert self.s.bucket_for(closeipp)[hash.hexhash(closeipp)]
