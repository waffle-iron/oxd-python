import json
import socket

from collections import namedtuple


class Messenger:
    """A class which takes care of the socket communication with oxD Server.
    The object is initialized with the port number
    """
    def __init__(self, port=8099):
        """Constructor for Messenger

        Args:
            port (integer) - the port number to bind to the localhost, default
                             is 8099
        """
        self.host = 'localhost'
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __connect(self):
        """A helper function to make connection."""
        try:
            self.sock.connect((self.host, self.port))
        except socket.error:
            raise RuntimeError("Could not connect to oxd-server on port {}"
                               .format(self.port))

    def __json_object_hook(self, d):
        """function to customized the json.loads to return named tuple instead
        of a dict"""
        return namedtuple('response', d.keys())(*d.values())

    def __json2obj(self, data):
        """Helper function which converts the json string into a namedtuple
        so the reponse values can be accessed like objects instead of dicts"""
        return json.loads(data, object_hook=self.__json_object_hook)

    def send(self, command):
        """send function sends the command to the oxD server and recieves the
        response.

        Args:
            command (dict) - Dict representation of the JSON command string

        Returns:
            response (dict) - The JSON response from the oxD Server as a dict
        """
        cmd_string = json.dumps(command)
        msg_length = len(cmd_string)
        cmd = "{:04d}".format(msg_length) + cmd_string

        # Send the message the to the server
        totalsent = 0
        while totalsent < msg_length+4:
            try:
                sent = self.sock.send(cmd[totalsent:])
                totalsent = totalsent + sent
            except socket.error:
                self.__connect()

        # Check and recieve the response if available
        parts = []
        resp_length = 0
        recieved = 0
        done = False
        while not done:
            part = self.sock.recv(1024)
            if part == "":
                raise RuntimeError("Socket connection broken.")

            # Find out the length of the response
            if len(part) > 0 and resp_length == 0:
                resp_length = int(part[0:4])
                part = part[4:]

            # Set Done flag
            recieved = recieved + len(part)
            if recieved >= resp_length:
                done = True

            parts.append(part)

        response = "".join(parts)
        # return the JSON as a namedtuple object
        return self.__json2obj(response)
