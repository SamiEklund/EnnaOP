""" Module for command base class """
class Command(object):
    """ Base class for all irc bot command
        Contains common logic for all commands and methods that should be implemented in child class
    """
    commandStrings = ["undefined"]

    def execute(self, user, params):
        """
            Logic for command
            This method should be overriden in child classmethod
        """
        raise NotImplementedError

    def match_command(self, cmd):
        """ Checks if given string matches any of this commands command strings"""
        for alt in self.commandStrings:
            if cmd == alt:
                return True
        return False
