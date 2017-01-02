""" Module for subscribe command """

from command import Command
from Common.manga_parser import MangaParser

class Subscribe(Command):
    """ Logic for Subscribe command """

    commandStrings = ["subscribe", "sub", "s+"]

    def execute(self, user, params):
        if MangaParser.add_follower_to_manga(params[0], user):
            return "You are now following " + params[0]
        return "Sorry, something went wrong with Subscribe :("
