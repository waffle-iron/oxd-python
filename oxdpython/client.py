from .configurer import Configurer
from .messenger import Messenger
from .discovery import Discovery
from .register import Register


class Client:
    """Client is the main class that carries out the commands to talk with the
    oxD server. The oxD request commands are provided as class methods that
    can be called to send the command to the oxD server via socket and the
    reponse is returned as a dict by the called method.
    """

    def __init__(self, config_location):
        """Constructor of class Client
        Args:
            config_location (string) - The complete path of the location of
                the config file which is a modified conpy of the sample.cfg
                from this library
        """
        self.config = Configurer(config_location)

        self.oxd_port = int(self.config.get('oxd', 'port'))
        self.client_name = self.config.get('client', 'client_name')
        self.msgr = Messenger(self.oxd_port)
        self.redirect_uris = self.config.get('client', 'redirect_uris')

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
            issuer = self.config.get('provider', 'issuer')
            url = "{}/.well-known/openid-configuration".format(issuer)
            cmd_class = Discovery(url)
        elif command == 'register':
            cmd_class = Register(self.metadata)

        resp = self.msgr.send(cmd_class.msg)
        return self.__data_or_error(resp)
