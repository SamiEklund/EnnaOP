""" Module for adding new manga to manga.json command """

from command import Command
from Common.manga_parser import MangaParser

class AddManga(Command):
    """ Logic for AddManga command """

    commandStrings = ["addmanga"]

    def execute(self, user, params):
        if MangaParser.monitor_new_manga(params[0]):
            return "We are now monitoring " + params[0] + "!"
        return "StupidUserError"
