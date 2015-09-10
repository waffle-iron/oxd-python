from nose.tools import assert_equal

from oxdpython import Client

issuer = 'https://gluu.example.com'


def test_initialization():
    """tests the discovery command of the client"""
    c = Client(issuer)
    assert_equal(c.issuer, issuer)
    assert_equal(c.oxd_port, 8099)

    c2 = Client(issuer, oxd_port=8888)
    assert_equal(c2.issuer, issuer)
    assert_equal(c2.oxd_port, 8888)
