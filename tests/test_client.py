import os

from nose.tools import assert_equal, assert_is_instance, assert_true,\
    assert_regexp_matches, assert_raises
from mock import patch

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


def test_client_raises_runtime_error_for_oxd_error_response():
    config = os.path.join(this_dir, 'data', 'no_oxdid.cfg')
    c = Client(config)
    with assert_raises(RuntimeError):
        c.register_site()


def test_client_can_get_authorization_url():
    c = Client(config_location)
    auth_url = c.get_authorization_url()

    assert_regexp_matches(auth_url, 'client_id')
    assert_regexp_matches(auth_url, 'response_type')
    assert_regexp_matches(auth_url, 'redirect_uri')


@patch.object(Messenger, 'send')
def test_client_get_tokens_by_code(mock_send):
    c = Client(config_location)
    code = "code"
    state = "state"
    scopes = ["openid"]
    command = {"command": "get_tokens_by_code",
               "params": {
                   "oxd_id": c.oxd_id,
                   "code": code,
                   "state": state,
                   "scopes": scopes
                   }}
    c.get_tokens_by_code(code, scopes, state)
    mock_send.assert_called_with(command)


@patch.object(Messenger, 'send')
def test_client_get_tokens_raises_error_for_invalid_args(mock_send):
    c = Client(config_location)
    # Empty code should raise error
    with assert_raises(RuntimeError):
        c.get_tokens_by_code("", ["openid"], "state")

    # Empty list for scopes should raise error
    with assert_raises(RuntimeError):
        c.get_tokens_by_code("code", [], "state")

    # raise error when scopes is not a list
    with assert_raises(RuntimeError):
        c.get_tokens_by_code("code", "openid", "state")


@patch.object(Messenger, 'send')
def test_client_get_user_info(mock_send):
    c = Client(config_location)
    code = "tokken"
    command = {"command": "get_user_info",
               "params": {
                   "oxd_id": c.oxd_id,
                   "access_code": code
                   }}
    c.get_user_info(code)
    mock_send.assert_called_with(command)


@patch.object(Messenger, 'send')
def test_client_get_user_info_raises_erro_on_invalid_args(mock_send):
    c = Client(config_location)
    # Empty code should raise error
    with assert_raises(RuntimeError):
        c.get_user_info("")
