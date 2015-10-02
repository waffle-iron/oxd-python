from .configurer import Configurer
from .messenger import Messenger


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
        self.msgr = Messenger(int(self.config.get('oxd', 'port')))
        self.application_type = self.config.get("client", "app_type")
        self.primary_redirect_uri = self.config.get("client",
                                                    "primary_redirect_uri")
        uris_val = self.config.get("client", "redirect_uris")
        self.redirect_uris = uris_val.split(",")

    def register_site(self):
        """Function to register the site and generate a unique ID for the site

        Args:
            None

        Returns:
            status (boolean) - Registration of site was successful or not
        """
        command = {"command": "register_site"}
        params = {"application_type": self.application_type,
                  "redirect_uris": self.redirect_uris,
                  "authorization_redirect_uri": self.primary_redirect_uri,
                  }
        command["params"] = params
        response = self.msgr.send(command)

        if response.status != 'ok':
            return False

        self.oxd_id = response.data.oxd_id
        self.config.set("oxd", "id", self.oxd_id)
        return True

    def get_authorization_url(self):
        """Function to get the authorization url that can be opened in the
        browser for the user to provide authorization and authentication

        Args:
            None

        Returns:
            auth_url (string) - the authorization url that the user must access
                                for authentication and authorization
        """
        command = {"command": "get_authorization_url"}
        params = {"oxd_id": self.oxd_id}
        command["params"] = params
        response = self.msgr.send(command)

        return response.data.authorization_url
