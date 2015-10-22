# oxd-python
Python Client Library for the [Gluu oxD Server RP](http://ox.gluu.org/doku.php?id=oxd:rp).

**oxdpython** is a thin wrapper around the communication protocol of oxD server. This can be used to access the OpenID connect & UMA Authorization end points of the Gluu Server via the oxD RP. This library provides the function calls required by a website to access user information from a OpenID Connect Provider (OP) by using the OxD as the Relying Party (RP).

## Using the Library in your website

[oxD RP](http://ox.gluu.org/doku.php?id=oxd:rp) has complete information about the Code Authorization flow and the various details about oxD RP configuration. This document provides only documentation about the oxd-python library.

### Prerequisites

* Install `gluu-oxd-server`

### Configuring

Create a copy of the sample configuration file for your website in a server *writable* location. The website is registered with the OP and its ID is stored in this config file, also are the other peristant information about the website. So the config file needs to be *writable* for the server. The `sample.cfg` file contains complete documentation about itself.


### Importing

The `Client` class of the library provides all the required methods required for the website to communicate with the oxD RP through sockets.

```
from oxdpython import Client

config = "/var/www/demosite/demosite.cfg"  # This should be writable by the server
client = Client(config)
```

### Website Registration

The website can be registered with the OP using the `client.register_client()` call. This can be skipped as any `get_authorization_url()` automatically registers the site if it is not.

### Get Authorization URL

The first step is to generate an authorization url which the user can visit to authorize your application to use the information from the OP.

```
auth_url = client.get_authorization_url()
```
Using the above url the website can redirect the user for authentication can authorization at the OP.

### Get access token

The website needs to parse the information fromt the callback url and pass it on to get the access token for fetching user information.

```
token = client.get_tokens_by_code(code, scopes, state)
```
The values for code, scope and state are parsed from the callback url querystring. Refer to your web framework to how to get these values from the url.

### Get user claims

Claims (information fields) made availble by the OP can be fethed using the access token obtained above.

```
user = oxc.get_user_info(token)
```

### Using the claims

The claims can be accessed using the dot notation.
```
print user.username
print user.inum
print user.website
```
The availability of varios claims are completely dependent on the OP. Listing the fields of user can give list of all the available claims.

```
print user._fields  # to print all the fields

# to check for a particular field and get the information
if 'website' in user._fields:
    print getattr(user, 'website')  # or
    print user.website
```

## Demo Site

The **demosite** folder contains a demo Flask application which uses the `oxdpython` library to demonstrate the usage of the library. Read throught the code at `demosite.py` for a better understanding of how a website can use the library. The deployment instrctions for the demosite can be found inside the demosite's README.


