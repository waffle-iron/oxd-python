from nose.tools import assert_equal

from oxdpython import Client

host = 'https://seed.gluu.org'


def test_discovery():
    """tests the discovery command of the client"""
    c = Client()
    response = c.discovery(host+"/.well-known/openid-configuration")
    assert_equal(response.status, 'ok')
    assert response.data
    assert_equal(response.data.issuer, 'https://seed.gluu.org')
