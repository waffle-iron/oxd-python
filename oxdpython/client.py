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
        self.authorization_redirect_uri = self.config.get(
            "client",
            "authorization_redirect_uri")
        self.oxd_id = None
        if self.config.get("oxd", "id"):
            self.oxd_id = self.config.get("oxd", "id")

    def __clear_data(self, response):
        """A private method that verifies that the oxd response is error free
        and raises a RuntimeError when it encounters an error
        """
        if response.status == "error":
            error = "OxD Server Error: {0}\nDescription:{1}".format(
                    response.data.error, response.data.error_description)
            raise RuntimeError(error)
        elif response.status == "ok":
            return response.data

    def register_site(self):
        """Function to register the site and generate a unique ID for the site

        Args:
            None

        Returns:
            status (boolean) - Registration of site was successful or not
        """
        command = {"command": "register_site"}

        # add required params for the command
        params = {"authorization_redirect_uri":
                  self.authorization_redirect_uri}
        # add other optional params if they exist in config
        opt_params = ["logout_redirect_uri", "client_jwks_uri",
                      "client_token_endpoint_auth_method"]
        opt_list_params = ["acr_values", "redirect_uris", "contacts",
                           "client_request_uris"]
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

        self.oxd_id = self.__clear_data(response).oxd_id
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

        return self.__clear_data(response).authorization_url

    def get_tokens_by_code(self, code, scopes, state=None):
        """Function to get access code for getting the user details from the
        OP. It is called after the user authorizies by visiting the auth URL.

        Args:
            code (string) - code obtained from the auth url callback
            scopes (list) - scopes authorized by the OP, fromt he url callback
            state (string) - state key obtained from the auth url callback

        Returns:
            access_token (string) - the access token which should be passed to
                                    get the user information from the OP
        """
        if not (code and scopes) or type(scopes) != list:
            raise RuntimeError("Empty code or scopes value.\n"
                               "Code: {0}\nScopes: {1}".format(code, scopes))

        command = {"command": "get_tokens_by_code"}
        params = {"oxd_id": self.oxd_id}
        params["code"] = code
        params["scopes"] = scopes

        if state:
            params["state"] = state

        command["params"] = params
        response = self.msgr.send(command)

        return self.__clear_data(response).access_token

    def get_tokens_by_code_by_url(self, url):
        """Function to get access code for getting the user details from the
        OP. It is called after the user authorizies by visiting the auth URL.

        Args:
            url (string) - the callback url which was called by the OP after
                           user authorization which has the states, code and
                           scopes as query parameters

        Returns:
            access_token (string) - the access token which should be passed to
                                    get the user information from the OP
        """
        command = {"command": "get_tokens_by_code"}
        params = {"oxd_id": self.oxd_id, "url": url}
        command["params"] = params
        response = self.msgr.send(command)

        return self.__clear_data(response).access_token

    def get_user_info(self, access_token):
        """Function to get the information about the user using the access code
        obtained from the OP

        Args:
            access_token (string) - access token from the get_tokens_by_code
                                    function

        Returns:
            claims (object) - the user data claims that are returned by the OP
        """
        if not access_token:
            raise RuntimeError("Empty access code")

        command = {"command": "get_user_info"}
        params = {"oxd_id": self.oxd_id}
        params["access_token"] = access_token
        command["params"] = params
        response = self.msgr.send(command)
        return self.__clear_data(response).claims
