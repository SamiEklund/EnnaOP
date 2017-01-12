""" Module for adding new manga to manga.json command """

from Commands.command import Command
from Common.manga_parser import MangaParser
from Common.manga import Manga

class AddManga(Command):
    """ Logic for AddManga command """

    commandStrings = ["addmanga"]

    def execute(self, user, params):
        manga = MangaParser.get_manga_by_title(params[0])
        if manga is None:
            new_manga = Manga(params[0])
            MangaParser.manga_list.append(new_manga)
            MangaParser.save_to_file()
            return "We are now monitoring " + params[0] + "!"
        return "Something went horribly wrong!"
