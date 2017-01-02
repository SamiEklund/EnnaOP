""" Module for subscribe command """

from command import Command
from Common.manga_parser import MangaParser

class Subscribe(Command):
    """ Logic for Subscribe command """

    commandStrings = ["subscribe", "sub", "s+"]

    def execute(self, user, params):
        MangaParser.add_follower_to_manga(params[0], user)
        return "I did a thing!"
