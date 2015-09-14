from nose.tools import assert_equal

from oxdpython import Client

issuer = 'https://gluu.example.com'
redirects = ['app.example.com', 'app.example.com/user/']


def test_initialization():
    """tests the discovery command of the client"""
    c = Client(issuer, redirects)
    assert_equal(c.issuer, issuer)
    assert_equal(c.oxd_port, 8099)

    c2 = Client(issuer, redirects, oxd_port=8888)
    assert_equal(c2.issuer, issuer)
    assert_equal(c2.oxd_port, 8888)


def test_client_discovery():
    c = Client(issuer, redirects)
    discovered = c.execute('discovery')
    assert_equal(discovered.issuer, issuer)
