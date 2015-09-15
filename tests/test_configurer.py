import os.path
from nose.tools import assert_true, assert_equal, assert_is_none

from oxdpython.configurer import Configurer

location = os.path.dirname(os.path.realpath(__file__))


def test_oxdconfig_looks_for_config_file_while_initialization():
    config = Configurer(location)
    assert_true(os.path.isfile(config.client_file))


def test_get_function_returns_value_for_set_config_value():
    config = Configurer(location)
    # for a set value it should be the set value
    assert_equal(config.get('oxd', 'port'), '8099')

    # for an unset value it should be none
    assert_is_none(config.get('oxd', 'message'))
    assert_is_none(config.get('two', 'coffee'))
