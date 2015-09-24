import os

from nose.tools import assert_equal, assert_is_instance

from oxdpython import Client
from oxdpython.messenger import Messenger

this_dir = os.path.dirname(os.path.realpath(__file__))
config_location = os.path.join(this_dir, 'data', 'initial.cfg')


def test_client_initializes_with_config():
    c = Client(config_location)
    assert_equal(c.config.get('oxd', 'port'), '8090')
    assert_is_instance(c.msgr, Messenger)
