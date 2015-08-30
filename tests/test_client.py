from nose.tools import assert_in

from oxdpython import Client


def test_discovery():
    """tests the discovery command of the client"""
    c = Client()
    response = c.discovery("http://ox.example.com/well/known/url")
    assert_in('status', response.keys())
    assert_in('data', response.keys())
