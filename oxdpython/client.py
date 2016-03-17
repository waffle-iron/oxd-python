import logging

from .configurer import Configurer
from .messenger import Messenger

logger = logging.getLogger(__name__)


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
            "client", "authorization_redirect_uri")
        self.oxd_id = None
        if self.config.get("oxd", "id"):
            self.oxd_id = self.config.get("oxd", "id")

            logger.info("Oxd ID found during initialization. Client is"
                        " already registered with the OpenID Provider")
            logger.info("oxd id: %s", self.oxd_id)

    def __clear_data(self, response):
        """A private method that verifies that the oxd response is error free
        and raises a RuntimeError when it encounters an error
        """
        if response.status == "error":
            error = "OxD Server Error: {0}\nDescription:{1}".format(
                    response.data.error, response.data.error_description)
            logger.error(error)
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
        if self.oxd_id:
            logger.info('Client is already registered. ID: %s', self.oxd_id)
            return self.oxd_id

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
        logger.debug("Sending command `register_site` with params %s",
                     params)
        response = self.msgr.send(command)
        logger.debug("Recieved reponse: %s", response)

        self.oxd_id = self.__clear_data(response).oxd_id
        self.config.set("oxd", "id", self.oxd_id)
        logger.info("Site registration successful. Oxd ID: %s", self.oxd_id)
        return self.oxd_id

    def get_authorization_url(self, acr_values=None):
        """Function to get the authorization url that can be opened in the
        browser for the user to provide authorization and authentication

        Args:
            acr_values (list) - OPTIONAL list of acr values in the order of
                                priority

        Returns:
            auth_url (string) - the authorization url that the user must access
                                for authentication and authorization
        """
        command = {"command": "get_authorization_url"}
        if not self.oxd_id:
            self.register_site()

        params = {"oxd_id": self.oxd_id}

        if acr_values and isinstance(acr_values, list):
            params["acr_values"] = acr_values

        command["params"] = params
        logger.debug("Sending command `get_authorization_url` with params %s",
                     params)
        response = self.msgr.send(command)
        logger.debug("Recieved reponse: %s", response)

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
            err_msg = """Empty/Wrong value in place of code or scope.
                      Code (string): {0}
                      Scopes (list): {1}""".format(code, scopes)
            logger.error(err_msg)
            raise RuntimeError(err_msg)

        command = {"command": "get_tokens_by_code"}
        params = {"oxd_id": self.oxd_id}
        params["code"] = code
        params["scopes"] = scopes

        if state:
            params["state"] = state

        command["params"] = params
        logger.debug("Sending command `get_tokens_by_code` with params %s",
                     params)
        response = self.msgr.send(command)
        logger.debug("Recieved reponse: %s", response)

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
        logger.debug("Sending command `get_tokens_by_code` with params %s",
                     params)
        response = self.msgr.send(command)
        logger.debug("Recieved reponse: %s", response)

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
            logger.error("Empty access code sent for get_user_info")
            raise RuntimeError("Empty access code")

        command = {"command": "get_user_info"}
        params = {"oxd_id": self.oxd_id}
        params["access_token"] = access_token
        command["params"] = params
        logger.debug("Sending command `get_user_info` with params %s",
                     params)
        response = self.msgr.send(command)
        logger.debug("Recieved reponse: %s", response)

        return self.__clear_data(response).claims

    def get_logout_uri(self, id_token_hint=None, post_logout_redirect_uri=None,
                       state=None, session_state=None):
        """Function to logout the user.

        Args:
            id_token_hint (string) - OPTIONAL (oxd server will use last used
                                     ID Token)
            post_logout_redirect_uri (string) - OPTIONAL URI for redirection,
                this uri would override the value given in the site-config
            state (string) - OPTIONAL site state
            session_state (string) - OPTIONAL session state
        Returns:
            uri (string) - the URI to which the user must be directed in
                           order to perform the logout
        """
        command = {"command": "get_logout_uri"}
        params = {"oxd_id": self.oxd_id}
        if id_token_hint:
            params["id_token_hint"] = id_token_hint

        if post_logout_redirect_uri:
            params["post_logout_redirect_uri"] = post_logout_redirect_uri
        elif self.config.get("client", "logout_redirect_uri"):
            params["post_logout_redirect_uri"] = self.config.get(
                "client", "logout_redirect_uri"
                )

        if state:
            params["state"] = state

        if session_state:
            params["session_state"] = session_state

        command["params"] = params

        logger.debug("Sending command `get_logout_uri` with params %s", params)
        response = self.msgr.send(command)
        logger.debug("Recieved response: %s", response)

        return self.__clear_data(response).uri

    def update_site_registration(self):
        """Fucntion to update the site's information with OpenID Provider.
        This should be called after changing the values in the cfg file.

        Args:
            None

        Returns:
            status (boolean) - Update of information was sucessful or not
        """
        command = {"command": "update_site_registration"}
        params = {"oxd_id": self.oxd_id,
                  "authorization_redirect_uri": self.authorization_redirect_uri
                  }
        optional_params = ["post_logout_redirect_uri", "application_type",
                           "client_jwks_uri",
                           "client_token_endpoint_auth_method"]
        optional_list_params = ["client_logout_uris", "grant_types",
                                "redirect_uris", "acr_values",
                                "client_reqeust_uris", "contacts"]
        for param in optional_params:
            if self.config.get("client", param):
                value = self.config.get("client", param)
                params[param] = value

        for param in optional_list_params:
            if self.config.get("client", param):
                value = self.config.get("client", param).split(",")
                params[param] = value

        command["params"] = params
        logger.debug("Sending command `register_site` with params %s",
                     params)
        response = self.msgr.send(command)
        logger.debug("Recieved reponse: %s", response)

        if response.status == "ok":
            return True
        else:
            return False
