# module metadata
__description__ = "A Python Client for oxD Server"
__version__ = "master"
__author__ = "Gluu"

# setup logging system
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

# expose Client
from client import Client
