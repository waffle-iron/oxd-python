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
        self.application_type = self.config.get("client", "application_type")
        self.authorization_redirect_uri = self.config.get("client",
                                                "authorization_redirect_uri")
        self.oxd_id = None
        if self.config.get("oxd", "id"):
            self.oxd_id = self.config.get("oxd", "id")

    def register_site(self):
        """Function to register the site and generate a unique ID for the site

        Args:
            None

        Returns:
            status (boolean) - Registration of site was successful or not
        """
        command = {"command": "register_site"}

        # add required params for the command
        params = {"authorization_redirect_uri": self.authorization_redirect_uri}
        # add other optional params if they exist in config
        opt_params = ["logout_redirect_uri", "client_jwks_uri",
                      "client_token_endpoint_auth_method"]
        opt_list_params = ["acr_values", "redirect_uris", "client_request_uris", "contacts"]
        for param in opt_params:
            if self.config.get("client", param):
                value = self.config.get("client", param)
                params[param] = value

        for param in opt_list_params:
            if self.config.get("client", param):
                value = self.config.get("client", param).split(",")
                params[param] = value

        command["params"] = params
        response = self.msgr.send(command)

        if response.status == "error":
            error = "OxD Server Error: {0}\nDescription:{1}".format(
                    response.data.error, response.data.error_description)
            raise RuntimeError(error)

        self.oxd_id = response.data.oxd_id
        self.config.set("oxd", "id", self.oxd_id)

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
        if not self.oxd_id:
            self.register_site()

        params = {"oxd_id": self.oxd_id}

        command["params"] = params
        response = self.msgr.send(command)

        if response.status == "error":
            error = "OxD Server Error: {0}\nDescription:{1}".format(
                    response.data.error, response.data.error_description)
            raise RuntimeError(error)

        return response.data.authorization_url
