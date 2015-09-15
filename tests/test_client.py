import os

from nose.tools import assert_equal

from oxdpython import Client

issuer = 'https://gluu.example.com'
redirects = ['https://client.example.com/callback',
             'https://client.example.com/callback2']

this_dir = os.path.dirname(os.path.realpath(__file__))
config_location = os.path.join(this_dir, 'data', 'initial.cfg')


def test_client_initializes_with_config():
    c = Client(config_location)
    assert_equal(c.client_name, 'oxD Python Test Client')
    assert_equal(c.oxd_port, 8099)


def notest_client_metadata_matches_config_file_values():
    c = Client(config_location)
    response_types = ['code', 'token', 'id_token', 'code token',
                      'code id_token', 'id_token token', 'code id_token token']
    grant_types = ['authorization_code', 'implicit', 'refresh_token']
    application_type = 'web'  # native not available for oxD
    contacts = ['arun@gluu.org', 'mike@gluu.org']
    client_name = 'oxD Python Test Client'

    assert_equal(c.response_types, response_types)
    assert_equal(c.grant_types, grant_types)
    assert_equal(c.application_type, application_type)
    assert_equal(c.contacts, contacts)
    assert_equal(c.client_name, client_name)


def test_client_discovery():
    c = Client(config_location)
    discovered = c.execute('discovery')
    assert_equal(discovered.issuer, issuer)


def notest_client_registration():
    c = Client(issuer, redirects, client_name="oxD Python Test",
               response_types="code id_token token",  # TODO update to list
               app_type="web",
               grant_types="authorization_code implicit",
               redirect_url="https://rs.gluu.org/resources",
               )
    registered = c.execute('register')
    assert registered.client_id
