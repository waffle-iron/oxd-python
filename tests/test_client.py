import os

from nose.tools import assert_equal, assert_is_instance, assert_true,\
    assert_raises, assert_is_none, assert_is_not_none
from mock import patch

from oxdpython import Client
from oxdpython.messenger import Messenger

this_dir = os.path.dirname(os.path.realpath(__file__))
config_location = os.path.join(this_dir, 'data', 'initial.cfg')


def test_initializes_with_config():
    c = Client(config_location)
    assert_equal(c.config.get('oxd', 'port'), '8099')
    assert_is_instance(c.msgr, Messenger)
    assert_equal(c.application_type, "web")
    assert_equal(c.authorization_redirect_uri,
                 "https://client.example.com/callback")
    assert_is_instance(c.oxd_id, str)


def test_register_site_command():
    # preset register client command response
    c = Client(config_location)
    c.oxd_id = None
    assert_is_none(c.oxd_id)
    c.register_site()
    assert_is_not_none(c.oxd_id)

"""
@patch.object(Messenger, 'send')
def test_register_raises_runtime_error_for_oxd_error_response(mock_send):
    mock_send.return_value.status = "error"
    mock_send.return_value.data.error = "MockError"
    mock_send.return_value.data.error_description = "MockError created to test"
    config = os.path.join(this_dir, 'data', 'no_oxdid.cfg')
    c = Client(config)
    with assert_raises(RuntimeError):
        c.register_site()


@patch.object(Messenger, 'send')
def test_get_authorization_url(mock_send):
    c = Client(config_location)
    mock_send.return_value.status = "ok"
    mock_send.return_value.data.authorization_url = "mock_url"
    command = {"command": "get_authorization_url",
               "params": {
                   "oxd_id": c.oxd_id
                   }}
    auth_url = c.get_authorization_url()
    mock_send.assert_called_with(command)
    assert_equal(auth_url, "mock_url")


@patch.object(Client, 'register_site')
@patch.object(Messenger, 'send')
def test_get_authorization_url_calls_register_if_no_oxdid(mock_send, mock_register):
    config_loc = os.path.join(this_dir, 'data', 'no_oxdid.cfg')
    c = Client(config_loc)
    mock_send.return_value.status = "ok"
    mock_send.return_value.data.authorization_url = "mock_url"
    c.get_authorization_url()
    mock_register.assert_called_with()


@patch.object(Messenger, 'send')
def test_get_auth_url_accepts_acr_as_optional_params(mock_send):
    c = Client(config_location)
    mock_send.return_value.status = "ok"
    mock_send.return_value.data.authorization_url = "mock_url"
    command = {"command": "get_authorization_url",
               "params": {
                   "oxd_id": c.oxd_id,
                   "acr_values": ["basic", "gplus"]
                   }}
    auth_url = c.get_authorization_url(["basic", "gplus"])
    mock_send.assert_called_with(command)
    assert_equal(auth_url, "mock_url")


@patch.object(Messenger, 'send')
def test_get_tokens_by_code(mock_send):
    c = Client(config_location)
    mock_send.return_value.status = "ok"
    mock_send.return_value.data.access_token = "mock-token"
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
    access_token = c.get_tokens_by_code(code, scopes, state)
    mock_send.assert_called_with(command)
    assert_equal(access_token, "mock-token")


def test_get_tokens_raises_error_for_invalid_args():
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
def test_get_tokens_by_code_by_url(mock_send):
    c = Client(config_location)
    mock_send.return_value.status = "ok"
    mock_send.return_value.data.access_token = "mock-token"
    url = "https://client.example.com/callback#state=demo123&code=d1e2m3o4"\
          "&scopes=openid%20profile"
    command = {"command": "get_tokens_by_code",
               "params": {
                   "oxd_id": c.oxd_id,
                   "url": url
                   }}
    access_token = c.get_tokens_by_code_by_url(url)
    mock_send.assert_called_with(command)
    assert_equal(access_token, "mock-token")


@patch.object(Messenger, 'send')
def test_get_tokens_raises_error_if_response_has_error(mock_send):
    c = Client(config_location)
    mock_send.return_value.status = "error"
    mock_send.return_value.data.error = "MockError"
    mock_send.return_value.data.error_description = "No Tokens in Mock"

    with assert_raises(RuntimeError):
        c.get_tokens_by_code("code", ["openid"], "state")


@patch.object(Messenger, 'send')
def test_get_user_info(mock_send):
    c = Client(config_location)
    mock_send.return_value.status = "ok"
    mock_send.return_value.data.claims = {"name": "mocky"}
    token = "tokken"
    command = {"command": "get_user_info",
               "params": {
                   "oxd_id": c.oxd_id,
                   "access_token": token
                   }}
    claims = c.get_user_info(token)
    mock_send.assert_called_with(command)
    assert_equal(claims, {"name": "mocky"})


def test_get_user_info_raises_erro_on_invalid_args():
    c = Client(config_location)
    # Empty code should raise error
    with assert_raises(RuntimeError):
        c.get_user_info("")


@patch.object(Messenger, 'send')
def test_get_user_info_raises_error_on_oxd_error(mock_send):
    c = Client(config_location)
    mock_send.return_value.status = "error"
    mock_send.return_value.data.error = "MockError"
    mock_send.return_value.data.error_description = "No Claims for mock"

    with assert_raises(RuntimeError):
        c.get_user_info("some_token")


@patch.object(Messenger, 'send')
def test_logout(mock_send):
    c = Client(config_location)
    mock_send.return_value.status = "ok"
    mock_send.return_value.data.uri = "https://example.com/end_session"

    params = {"oxd_id": c.oxd_id}
    command = {"command": "get_logout_uri",
               "params": params}

    # called with no optional params
    uri = c.get_logout_uri()
    mock_send.assert_called_with(command)

    # called with OPTIONAL id_token_hint
    uri = c.get_logout_uri("some_id")
    command["params"]["id_token_hint"] = "some_id"
    mock_send.assert_called_with(command)
    assert_equal(uri, "https://example.com/end_session")

    # called wiht OPTIONAL id_token_hint + post_logout_redirect_uri
    uri = c.get_logout_uri("some_id", "https://some.site/logout")
    command["params"]["post_logout_redirect_uri"] = "https://some.site/logout"
    mock_send.assert_called_with(command)

    # called wiht OPTIONAL id_token_hint + post_logout_redirect_uri + state
    uri = c.get_logout_uri("some_id", "https://some.site/logout", "some-s")
    command["params"]["state"] = "some-s"
    mock_send.assert_called_with(command)

    # called wiht OPTIONAL id_token_hint + post_logout_redirect_uri
    uri = c.get_logout_uri("some_id", "https://some.site/logout", "some-s",
                           "some-ss")
    command["params"]["session_state"] = "some-ss"
    mock_send.assert_called_with(command)


@patch.object(Messenger, 'send')
def test_logout_raises_error_when_oxd_return_error(mock_send):
    c = Client(config_location)
    mock_send.return_value.status = "error"
    mock_send.return_value.data.error = "MockError"
    mock_send.return_value.data.error_description = "Logout Mock Error"

    with assert_raises(RuntimeError):
        c.get_logout_uri()


@patch.object(Messenger, 'send')
def test_update_site_registration(mock_send):
    c = Client(config_location)
    mock_send.return_value.status = "ok"

    params = {"oxd_id": c.oxd_id,
              "application_type": c.config.get("client", "application_type"),
              "authorization_redirect_uri":
              c.config.get("client", "authorization_redirect_uri"),
              "redirect_uris": ["https://client.example.com/callback",
                                "https://client.example.com/callback2"]
              }
    command = {"command": "update_site_registration",
               "params": params}

    status = c.update_site_registration()
    mock_send.assert_called_with(command)
    assert_true(status)
"""
