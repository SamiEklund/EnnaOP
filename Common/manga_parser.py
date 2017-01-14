""" """

import json
import jsonpickle

from Common.manga import Manga
from Common.chapter import Chapter

def load_manga_file():
    """ Reads saved status from JSON file """
    try:
        manga_file = open("manga.json", "r")
        manga_list = jsonpickle.decode(manga_file.read())
        manga_file.close()
    except IOError:
        manga_list = []

    return manga_list

class MangaParser(object):
    """ Static class for handling manga list instance
        The only file that will communicate with the JSON file
    """

    sourceList = None
    manga_list = load_manga_file()

    @staticmethod
    def save_to_file():
        """ Saves the MangaParser.manga_file instance to a JSON file """
        manga_file = open("manga.json", "w")
        json_data = jsonpickle.encode(MangaParser.manga_list)
        json_data = json.loads(json_data)
        json.dump(json_data, manga_file, indent=4, sort_keys=True, separators=(',', ':'))
        manga_file.close()

    @staticmethod
    def get_manga_by_title(manga_title):
        """ Returns manga object by title """
        for manga in MangaParser.manga_list:
            if manga.name.lower() == manga_title.lower():
                return manga
        return None

    @staticmethod
    def check_for_new_releases(release_list):
        """ Compares release_list to manga_list and updates any new releases """
        if not release_list:
            return []

        new_releases = []

        for new_manga in release_list:
            manga = MangaParser.get_manga_by_title(new_manga.name)

            if manga and manga.update_chapter(new_manga.chapter):
                new_releases.append(manga)

        if len(new_releases) > 0:
            MangaParser.save_to_file()

        return new_releases
