from .messenger import Messenger


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

    def discovery(self, url):
        """Runs the discovery command on the oxD server.

        Args:
            url (string) - the 'discovery_url' parameter for the command

        Returns:
            response (dict) - the JSON response from the server as a dict
        """
        command = {"command": "discovery",
                   "params": {
                       "discovery_url": url
                       }
                   }
        response = self.msgr.send(command)
        return response
