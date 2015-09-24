import os.path
from nose.tools import assert_true, assert_equal, assert_is_none

from oxdpython.configurer import Configurer

this_dir = os.path.dirname(os.path.realpath(__file__))
location = os.path.join(this_dir, 'data', 'initial.cfg')


def test_oxdconfig_looks_for_config_file_while_initialization():
    config = Configurer(location)
    assert_true(os.path.isfile(config.config_file))


def test_get_function_returns_value_for_set_config_value():
    config = Configurer(location)
    # for a set value it should be the set value
    assert_equal(config.get('oxd', 'port'), '8090')
    assert_equal(config.get('oxd', 'host'), 'localhost')

    # for an unset value it should be none
    assert_is_none(config.get('oxd', 'message'))
    assert_is_none(config.get('two', 'coffee'))
