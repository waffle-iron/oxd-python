from ConfigParser import SafeConfigParser, NoOptionError, NoSectionError


class Configurer(object):
    """The class which holds all the information about the client and the OP
    metadata"""
    def __init__(self, cfg_file):
        self.parser = SafeConfigParser()
        self.config_file = cfg_file
        self.parser.read(self.config_file)

    def get(self, section, key):
        """get function reads the config value for the requested section and
        key and returns it

        Args:
            section (string) - the section to look for the config value
                               either - oxd, client, provider
            key (string) - the key for the config value required

        Returns:
            value (multiple) - the function returns the value of the key
                               in the appropriate format if found or returns
                               None if such a section or key couldnot be found

        Example:
            config = Configurer(location)
            oxd_port = config.get('oxd', 'port')  # returns the port of the oxd
        """
        try:
            return self.parser.get(section, key)
        except (NoOptionError, NoSectionError):
            return None
