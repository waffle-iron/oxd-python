import os.path
from nose.tools import assert_true

from oxdpython.configurer import Configurer


def test_oxdconfig_looks_for_config_file_while_initialization():
    location = os.path.dirname(os.path.realpath(__file__))
    config = Configurer(location)
    assert_true(os.path.isfile(config.client_file))
