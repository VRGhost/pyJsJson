"""Test $ref command. """


def test_full_file_ref(UnittestFs, expand_data):
    UnittestFs.mockFile('/unittest/base.json', {'$ref': 'file:target.json'})
    UnittestFs.mockFile('/unittest/target.json', {'hello': 'world'})
    out = expand_data({'$ref': 'file:base.json'})
    assert out == {'hello': 'world'}
