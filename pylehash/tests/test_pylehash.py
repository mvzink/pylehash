'''
Created on Feb 7, 2011

@author: Michael Victor Zink <zuwiki@zuwiki.net>

TODO: Rename class fixture vars to be more informative
'''

from mock import Mock

from test_stuff import TestCase, selfipp, closeipp, closeipp2, closeipp3, mediumipp, faripp
from pylehash import hash, Telex, Switch, End, handlers, ippstr

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
        longval = 1073680171875912199119184443246291065335917135622
        assert hash.hexbin(hexval) == longval

    def test_binhash_arbitrary_string(self):
        longval = 1073680171875912199119184443246291065335917135622
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

    def test_distance_supports_hash_ipptuple_or_end(self):
        a = hash.distance(selfipp, faripp)
        b = hash.distance(hash.hexhash(selfipp), hash.hexhash(faripp))
        c = hash.distance(hash.hexhash(selfipp), faripp)
        d = hash.distance(selfipp, hash.hexhash(faripp))
        e = hash.distance(selfipp, End(faripp))
        f = hash.distance(End(selfipp), faripp)
        g = hash.distance(End(selfipp), End(faripp))
        assert a == b == c == d == e == f == g

class TestSwitch(TestCase):

    def setUp(self):
        self.s = Switch()
        self.s.ipp = selfipp

    def test_switch_complete_bootstrap(self):
        assert self.s.ipp == selfipp
        
    def test_switch_add_end_adds_end(self):
        self.s.add_end(End(closeipp))
        assert self.s.bucket_for(End(closeipp))[hash.hexhash(closeipp)]

    def test_switch_bucket_for_gives_correct_bucket(self):
        self.s.add_end(End(closeipp))
        o = self.s.bucket_for(End(closeipp))
        assert self.s.buckets.index(o) == hash.distance(selfipp, closeipp)
        self.s.add_end(End(faripp))
        p = self.s.bucket_for(End(faripp))
        assert self.s.buckets.index(p) == hash.distance(selfipp, faripp)

    def test_switch_send_writes_to_transport_iff_the_telex_is_not_empty(self):
        s = Switch()
        s.ipp = selfipp
        s.transport = Mock()
        s.transport.write = Mock()
        empty_tel = Telex()
        s.send(telex=empty_tel, to=End(faripp))
        assert not s.transport.write.called
        tel = Telex(other_dict={'+foo':'bar'})
        s.send(telex=tel, to=End(faripp))
        s.transport.write.assert_called_with(tel.dumps(), faripp)

    def test_switch_start_protocol_sends_bootstrap_telex_under_correct_conditions(self):
        s_should_send = Switch(seed_ipp=faripp)
        s_should_send.send = Mock()
        s_should_send.startProtocol()
        assert s_should_send.send.called
        s_should_not_send = Switch()
        s_should_not_send.ipp = selfipp
        s_should_not_send.send = Mock()
        s_should_not_send.startProtocol()
        assert not s_should_not_send.send.called


class TestEnd(TestCase):

    def test_end_inits_with_and_provides_access_to_ipp_tuple(self):
        e = End(closeipp)
        assert e.ipp == closeipp

    def test_end_tracks_bytes_received(self):
        e = End(closeipp)
        assert e.br == 0
        e.br += 52
        assert e.br == 52


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
        assert t.dumps() == '{"+test": "testing"}'


class TestHandler(TestCase):
    '''
    Essentially only tests the __call__ prototype for calling handler.matches
    and subsequently calling handler.handle iff handler.matches is true.
    '''
    def setUp(self):
        self.h = handlers.Handler()
        self.h.handle = Mock()
        self.h.matches = Mock()
        self.t = Telex()
        self.s = Switch()

    def test_handler_handle_is_called_if_it_matches(self):
        self.h.matches.return_value = True
        self.h(self.t, End(faripp), self.s)
        assert self.h.handle.called

    def test_handler_handle_is_not_called_if_it_doesnt_match(self):
        self.h.matches.return_value = False
        self.h(self.t, End(faripp), self.s)
        assert not self.h.handle.called

class TestTapHandler(TestCase):
    '''
    More than anything, this should serve as an example of how to write
    a handler class that conforms to the accepted protocol.
    See pylehash.handlers for TapHandler.
    '''

    def setUp(self):
        '''
        Defines a tap handler that should match any telex which either
            1. has both +foo and +bar signals, or
            2. has a +foo signal equal to "no_bar"
        '''
        self.t = handlers.TapHandler([
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

    def test_tap_handler_correctly_and_safely_tests_for_matching_telexes(self):
        assert self.t.matches(self.match_has, End(faripp), Switch())
        assert self.t.matches(self.match_is, End(faripp), Switch())
        assert self.t.matches(self.match_both, End(faripp), Switch())
        assert not self.t.matches(self.no_match, End(faripp), Switch())
    

class TestForwardingTapHandler(TestCase):
    
    def setUp(self):
        self.s = Switch()
        self.s.ipp = selfipp
        self.s.send = Mock()
        self.h = handlers.ForwardingTapHandler([
            {'has': ['+foo', '+bar']},
            {'is': {'+foo': 'no_bar'}}
        ], End(faripp))
        self.match_both = Telex(other_dict={
            '+foo': 'no_bar',
            '+bar': 'except_still_a_bar'
        })
        self.no_match = Telex(other_dict={
            '+foo': 'where_is_the_bar'
        })
        self.too_hopped_up = Telex(other_dict={
            '+foo': 'no_bar',
            '_hop': 5
        })

    def test_forwarding_tap_handler_forwards_matching_telex_when_called(self):
        # TODO: Also make sure the correct telex is being sent
        #   i.e. _hop increased, _br, etc. but otherwise the same
        self.h(self.match_both, End(closeipp), self.s)
        assert self.s.send.called

    def test_forwarding_tap_handler_does_not_forward_non_matching_telex(self):
        self.h(self.no_match, End(closeipp), self.s)
        assert not self.s.send.called

    def test_forwarding_tap_handler_does_not_forward_telex_with_too_many_hops(self):
        self.h(self.too_hopped_up, End(closeipp), self.s)
        assert not self.s.send.called

class TestEndHandler(TestCase):
    def setUp(self):
        self.seeking_far = Telex(other_dict={'+end': hash.hexhash(faripp)})
        self.from_end = End(closeipp)
        self.t = handlers.EndHandler()

    def test_end_handler_only_matches_telexes_with_end_signals(self):
        assert self.t.matches(self.seeking_far, End(faripp), Switch())

    def test_end_handler_sends_list_of_ends_to_original_sender(self):
        switch = Switch()
        switch.ipp = selfipp
        switch.add_end(End(faripp))
        switch.send = Mock()
        self.t(self.seeking_far, self.from_end, switch)
        assert switch.send.called
        tel = switch.send.call_args[-1]['telex']
        assert isinstance(tel, Telex)
        assert ippstr(faripp) in tel['.see']
        assert switch.send.call_args[-1]['to'] == self.from_end

class TestNewTapHandler(TestCase):
    def setUp(self):
        self.h = handlers.NewTapHandler()
        self.taptests = [{'has':['foo']}]
        self.new_tap_tel = Telex(other_dict={'.tap': self.taptests})
        self.s = Switch()

    def test_new_tap_handler_matches_tap_commands(self):
        assert self.h.matches(self.new_tap_tel, End(faripp), self.s)
        assert not self.h.matches(Telex(other_dict={'+foo':'bar'}), End(faripp), self.s)

    def test_new_tap_handler_appropriate_a_forwarding_tap_handler_to_switch(self):
        e = End(closeipp)
        self.h(self.new_tap_tel, e, self.s)
        is_correct_handler_type = lambda k: isinstance(k, handlers.ForwardingTapHandler)
        a = filter(is_correct_handler_type, self.s.handlers.values())
        assert a[0].to == e
        assert a[0].tests == self.taptests

class TestBootstrapHandler(TestCase):
    def setUp(self):
        self.h = handlers.BootstrapHandler(faripp)
        self.telex_with_to = Telex(other_dict={'_to': '127.0.0.1:5555'})
        self.telex_without_to = Telex(other_dict={'+foo': 'bar'})

    def test_bootstrap_handler_matches_telexes_from_seeder_with_to(self):
        assert self.h.matches(self.telex_with_to, End(faripp), Switch())

    def test_bootstrap_handler_does_not_match_telex_from_wrong_ipp(self):
        assert not self.h.matches(self.telex_with_to, End(closeipp), Switch())

    def test_bootstrap_handler_does_not_match_telex_with_no_to(self):
        assert not self.h.matches(self.telex_without_to, End(faripp), Switch())

    def test_bootstrap_handler_sets_switch_ipp(self):
        s = Switch()
        s.remove_handler = Mock()
        assert s.ipp == None
        self.h(self.telex_with_to, End(faripp), s)
        assert s.ipp == ('127.0.0.1', 5555)

    def test_bootstrap_handler_adds_other_default_handlers_and_removes_itself(self):
        s = Switch()
        s.handlers = {id(self.h): self.h}
        self.h(self.telex_with_to, End(faripp), s)
        assert len(s.handlers) > 0
        assert id(self.h) not in s.handlers

class TestSeeHandler(TestCase):

    def setUp(self):
        self.h = handlers.SeeHandler()
        self.s = Switch()
        self.s.ipp = selfipp
        self.s.add_end = Mock()
        self.t = Telex(other_dict={'.see': map(ippstr, [closeipp2, closeipp3, mediumipp])})
        self.no_match = Telex(other_dict={'+foo': 'bar'})

    def test_see_handler_matches_correctly(self):
        assert self.h.matches(self.t, End(closeipp), self.s)
        assert not self.h.matches(self.no_match, End(closeipp), self.s)

    def test_see_handler_tells_switch_to_add_ends(self):
        self.h(self.t, End(closeipp), self.s)
        assert self.s.add_end.called
