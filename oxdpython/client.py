from .messenger import Messenger
from .discovery import Discovery


class Client:
    """Client is the main class that carries out the commands to talk with the
    oxD server. The oxD request commands are provided as class methods that
    can be called to send the command to the oxD server via socket and the
    reponse is returned as a dict by the called method.
    """

    def __init__(self, issuer, oxd_port=8099):
        """Constructor of class Client
        Args:
            issuer (string) - URL of the issuer domain. e.g., gluu.example.com

            oxdport (integer) - Client is initialized with the port number at
                             which the oxD server is listening. It has a
                             default value 8099
        """
        self.issuer = issuer
        self.oxd_port = oxd_port
        self.msgr = Messenger(self.oxd_port)

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

        Returns:
            response (object) - the JSON response as an object
        """
        if command == 'discovery':
            d = Discovery(self.issuer)
            resp = self.msgr.send(d.msg)
            return self.__data_or_error(resp)
