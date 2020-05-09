"""Test $ref command. """
import pytest

import pyJsJson


def test_full_file_ref(UnittestFs, expand_data):
    UnittestFs.mockFile('/unittest/base.json', {'$ref': 'file:target.json'})
    UnittestFs.mockFile('/unittest/target.json', {'hello': 'world'})
    out = expand_data({'$ref': 'file:base.json'})
    assert out == {'hello': 'world'}


@pytest.mark.parametrize('path,exp_out', [
    ('top-key', {'sub-key': 'value'}),
    ('top-key/sub-key', 'value'),
])
def test_field_in_file_ref(UnittestFs, expand_data, path, exp_out):
    UnittestFs.mockFile('/unittest/target.json', {
        'top-key': {
            'sub-key': 'value'
        }
    })
    out = expand_data({
        '$ref': 'file:target.json#{}'.format(path)
    })
    assert out == exp_out


@pytest.mark.parametrize('uri', [
    'file:idontexist.json',
    'file:idontexist.json#key',
    'file:target.json#missing-key'
])
def test_missing_ref(UnittestFs, expand_data, uri):
    """Test that passing in incorrect ref uri raises an exception."""
    UnittestFs.mockFile('/unittest/target.json', {
        'top-key': {
            'sub-key': 'value'
        }
    })
    with pytest.raises(pyJsJson.exceptions.PyJsJsonException):
        expand_data({'$ref': uri})


def test_self_ref(UnittestFs, expand_data):
    out = expand_data({
        'value': 'hello-world',
        'output': {'$ref': '#/value'}
    })
    assert out['output'] == 'hello-world'
