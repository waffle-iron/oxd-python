from .messenger import Messenger
from .discovery import Discovery
from .register import Register


class Client:
    """Client is the main class that carries out the commands to talk with the
    oxD server. The oxD request commands are provided as class methods that
    can be called to send the command to the oxD server via socket and the
    reponse is returned as a dict by the called method.
    """

    def __init__(self, issuer, redirect_uris, oxd_port=8099, **kwargs):
        """Constructor of class Client
        Args:
            issuer (string) - Base URL of the Resource Provider
                              e.g., gluu.example.com

            redirect_uris (list) - list of redirect URIs values that will be
                                  used by the client. Passed with each auth
                                  request to the Resource Provider

            oxdport (integer) - Client is initialized with the port number at
                             which the oxD server is listening. It has a
                             default value 8099
            **kwargs - Other client metadata
        """
        self.issuer = issuer
        self.oxd_port = oxd_port
        self.msgr = Messenger(self.oxd_port)
        self.redirect_uris = redirect_uris
        self.metadata = kwargs
        self.metadata['discovery_url'] = "{}/.well-known/openid-configuration".\
            format(issuer)
        # FIXME fix the redirect urls with the oxD implemetation vs OIDC
        # self.metadata['redirect_uris'] = redirect_uris

        # TODO make accessing metadata better
        keys = kwargs.keys()
        for key in keys:
            setattr(self, key, kwargs[key])

    def __data_or_error(self, response):
        """Processes the OXD server response object and returns just the data
        """
        return response.data

    def execute(self, command):
        """Task executor based on the command recieved

        Args:
            command (string) - Any one of the known ODIC client side actions
                Available:
                1. discovery - discover information about OpenID Provider
                2. register - register the client with the OP

        Returns:
            response (object) - the JSON response as an object
        """
        if command == 'discovery':
            cmd_class = Discovery(self.metadata['discovery_url'])
        elif command == 'register':
            cmd_class = Register(self.metadata)

        resp = self.msgr.send(cmd_class.msg)
        return self.__data_or_error(resp)
