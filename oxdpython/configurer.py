import os

from ConfigParser import SafeConfigParser


class Configurer(object):
    """The class which holds all the information about the client and the OP
    metadata"""
    def __init__(self, location):
        self.parser = SafeConfigParser()
        self.client_file = os.path.join(location, 'oxdpython.cfg')

        # ensure the configuration file exists
        if not os.path.isfile(self.client_file):
            self.parser.add_section('client')
            with open(self.client_file, "w") as cfile:
                self.parser.write(cfile)

        self.parser.read(self.client_file)
