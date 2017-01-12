""" Module for unsubscribe command """

from Commands.command import Command
from Common.manga_parser import MangaParser

class Unsubscribe(Command):
    """ Logic for Unubscribe command """

    commandStrings = ["unsubscribe", "unsub", "s-", "-s"]

    def execute(self, user, params):
        manga = MangaParser.get_manga_by_title(params[0])
        if manga and manga.remove_follower(user):
            MangaParser.save_to_file()
            return "You won't get any notifications from " + params[0] + " anymore."
        return "Sorry, something went wrong with Subscribe :("