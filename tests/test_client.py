import os

from nose.tools import assert_equal, assert_is_instance, assert_true,\
    assert_regexp_matches, assert_raises

from oxdpython import Client
from oxdpython.messenger import Messenger

this_dir = os.path.dirname(os.path.realpath(__file__))
config_location = os.path.join(this_dir, 'data', 'initial.cfg')


def test_client_initializes_with_config():
    c = Client(config_location)
    assert_equal(c.config.get('oxd', 'port'), '8099')
    assert_is_instance(c.msgr, Messenger)
    assert_equal(c.application_type, "web")
    assert_equal(c.authorization_redirect_uri,
                 "https://client.example.com/callback")
    assert_is_instance(c.oxd_id, str)


def test_client_register_site_command():
    c = Client(config_location)
    c.oxd_id = None
    assert_equal(c.oxd_id, None)
    c.register_site()
    assert_true(len(c.oxd_id) > 0)


def test_client_can_get_authorization_url():
    c = Client(config_location)
    auth_url = c.get_authorization_url()
    assert_regexp_matches(auth_url, 'client_id')
    assert_regexp_matches(auth_url, 'response_type')
    assert_regexp_matches(auth_url, 'redirect_uri')
