""" Module for subscribe command """

from Commands.command import Command
from Common.manga_parser import MangaParser

class Subscribe(Command):
    """ Logic for Subscribe command """

    commandStrings = ["subscribe", "sub", "s+"]

    def execute(self, user, params):
        manga = MangaParser.get_manga_by_title(params[0])
        if manga and manga.add_follower(user):
            MangaParser.save_to_file()
            return "You are now following " + params[0]
        return "Sorry, something went wrong with Subscribe :("
