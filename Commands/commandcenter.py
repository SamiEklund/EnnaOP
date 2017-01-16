"""Module for handling all commands"""

from Commands.command_subscribe import Subscribe
from Commands.command_unsubscribe import Unsubscribe
from Commands.command_addmanga import AddManga
from Common.logger import Logger

class CommandCenter(object):
    """ Master of the commands TODO: Explain better """

    commands = [
        Subscribe(),
        Unsubscribe(),
        AddManga()
    ]

    COMMAND_PREFIX = "!"
    parameter_separator = "|"

    def parse_and_execute(self, user, message):
        """ Parses the command string and parameters from given message and executes it """
        if not message.startswith(self.COMMAND_PREFIX):
            return ""

        Logger.log("Valid command was given! User: %s Command: %s" % (user, message))
        command = self.parse_command(message)
        parameters = self.parse_parameters(message)

        if not command or len(parameters) is 0:
            return ""

        return self.execute_command(command, user, parameters)


    def parse_command(self, message):
        """ Parses command string from given message """
        start = message.index(self.COMMAND_PREFIX) + 1
        end = message.index(" ", start)
        return message[start:end]

    def parse_parameters(self, message):
        """ Parses parameters from given message """
        split_message = message.split(" ", 1)
        if  len(split_message) <= 1:
            return []

        return split_message[1].split(self.parameter_separator)

    def execute_command(self, command_str, user, params):
        """ Loops through all defined commands and executes the one matching given string """
        for command in self.commands:
            if command.match_command(command_str):
                return command.execute(user, params)
        return ""
