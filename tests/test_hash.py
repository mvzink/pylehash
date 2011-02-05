from pylehash.hash import hexhash, binhash, hexbin

def test_hexhash_arbitrary_string():
    test_hash = 'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3'
    assert hexhash('test') == test_hash

def test_hexhash_ipp_str():
    ipp_hash = 'bc117be99339576519af05e91d51376feabd4706'
    assert hexhash('127.0.0.1:5555') == ipp_hash

def test_hexhash_ipp_tuple():
    ipp_hash = 'bc117be99339576519af05e91d51376feabd4706'
    assert hexhash(('127.0.0.1',5555)) == ipp_hash

def test_hexbin_short():
    assert hexbin('e') == 14
    assert hexbin('abc123abc123') == 188846015496483

def test_hexbin_long():
    hexval = 'bc117be99339576519af05e91d51376feabd4706'
    longval = 1073680171875912199119184443246291065335917135622L
    assert hexbin(hexval) == longval

def test_binhash_arbitrary_string():
    longval = 1073680171875912199119184443246291065335917135622L
    assert binhash('127.0.0.1:5555') == longval
