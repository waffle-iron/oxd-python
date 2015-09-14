from nose.tools import assert_equal

from oxdpython import Client

issuer = 'https://gluu.example.com'
redirects = ['https://client.example.com/callback',
             'https://client.example.com/callback2']


def test_initialization_without_metadata():
    """tests the discovery command of the client"""
    c = Client(issuer, redirects)
    assert_equal(c.issuer, issuer)
    assert_equal(c.oxd_port, 8099)

    c2 = Client(issuer, redirects, oxd_port=8888)
    assert_equal(c2.issuer, issuer)
    assert_equal(c2.oxd_port, 8888)


def test_init_with_metadata():
    response_types = ['code', 'token', 'id_token', 'code token',
                      'code id_token', 'id_token token', 'code id_token token']
    grant_types = ['authorization_code', 'implicit', 'refresh_token']
    application_type = ['web']  # native not available for oxD
    contacts = ['arun@gluu.org', 'mike@gluu.org']
    client_name = 'oxD Python Test code'
    logo_uri = 'https://client.example.com/logo'
    client_uri = 'https://example.com'
    policy_uri = 'https://example.com/policy'
    tos_uri = 'https://example.com/tos'
    jwks_uri = 'https://example'

    c = Client(issuer, redirects,
               response_types=response_types,
               grant_types=grant_types,
               application_type=application_type,
               contacts=contacts,
               client_name=client_name,
               logo_uri=logo_uri,
               client_uri=client_uri,
               policy_uri=policy_uri,
               tos_uri=tos_uri,
               jwks_uri=jwks_uri
               )

    assert_equal(c.response_types, response_types)
    assert_equal(c.grant_types, grant_types)
    assert_equal(c.application_type, application_type)
    assert_equal(c.contacts, contacts)
    assert_equal(c.client_name, client_name)
    assert_equal(c.logo_uri, logo_uri)
    assert_equal(c.client_uri, client_uri)
    assert_equal(c.policy_uri, policy_uri)


def test_client_discovery():
    c = Client(issuer, redirects)
    discovered = c.execute('discovery')
    assert_equal(discovered.issuer, issuer)


def test_client_registration():
    c = Client(issuer, redirects, client_name="oxD Python Test",
               response_types="code id_token token",  # TODO update to list
               app_type="web",
               grant_types="authorization_code implicit",
               redirect_url="https://rs.gluu.org/resources",
               )
    registered = c.execute('register')
    assert registered.client_id
