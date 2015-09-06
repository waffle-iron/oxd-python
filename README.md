# oxd-python
Python Client Library for the [Gluu oxD Server](http://ox.gluu.org/doku.php?id=oxd:home).

**oxdpython** is a thin wrapper around the communication protocol of oxD server. This can be used to access the OpenID connect & UMA Authorization end points of the Gluu Server via the oxD.

**Note**: This library is merely a communication protocol wrapper for the oxd server usign socket communication and DOES NOT deal with the sanitization of data or other checks necessary for quality. The library assumes that such functionality would be performed by the oxD server before passing on the information to the Authorization end points of UMA and OIDC.
