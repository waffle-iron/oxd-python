from .messenger import Messenger


class Client:
    """Client is the main class that carries out the commands to talk with the
    oxD server. The oxD request commands are provided as class methods that
    can be called to send the command to the oxD server via socket and the 
    reponse is returned as a dict by the called method.
    """

    def __init__(self, port=8099):
        """Constructor of class Client
        Args:
            port (integer) - Client is initialized with the port number at
                             which the oxD server is listening. It has a
                             default value 8099
        """
        self.port = port
        self.msgr = Messenger(port)

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
        return self.msgr.send(command)
