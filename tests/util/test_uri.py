import pytest

from pyJsJson.util import URI


@pytest.mark.parametrize('inp', [
    'file:/test.json',
    'file:dir/test.json',
    'file:/dir/test.json',
    'file:test.json',
    'file:test.json#key',
    'file:test.json#key/subkey',
    '#key',
    '#key/subkey',
    'test.json',
    'test.json#key',
    '__tree__:potato#key',
    '__tree__:label:potato#key',
])
def test_simple_parse(inp):
    """An input URI that should produce exactly matching output."""
    assert URI.fromString(inp).toString() == inp


@pytest.mark.parametrize('inp,output', [
    (r'file://hello.json#key', 'file:hello.json#key'),
])
def test_parse_with_conversion(inp, output):
    """An input URI that should produce exactly matching output."""
    assert URI.fromString(inp).toString() == output


@pytest.mark.parametrize('inp,output', [
    ('', 'default-scheme:default-path#default-anchor'),
    ('user-scheme:', 'user-scheme:default-path#default-anchor'),
    ('path', 'default-scheme:path#default-anchor'),
    ('#just-key', 'default-scheme:default-path#just-key'),
])
def test_apply_defaults(inp, output):
    uri = URI.fromString(inp)
    newUri = uri.defaults(
        scheme='default-scheme',
        path='default-path',
        anchor='default-anchor'
    )
    assert newUri.toString() == output


def test_str_conv():
    uri_str = 's:p#k'
    uri = URI.fromString(uri_str)
    assert uri_str in str(uri)
    assert uri_str in repr(uri)
