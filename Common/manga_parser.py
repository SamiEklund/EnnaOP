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

"""
    FIXME: Reimplement these methods

    def checkForNewReleases(self):
        ircMessages = []

        for source in self.sourceList:
            newReleases = []
            releases = source.getManga()
            if not releases:
                continue
            for release in releases:
                manga = self.getMangaByTitle(release.mangaName)
                if manga and release.chapterNumber > manga.chapterNumber:
                    release.setFollowers(manga.followers)
                    newReleases.append(release)

            for release in newReleases:
                ircMessages.append(release.getMessage())
                manga = self.getMangaByTitle(release.mangaName)
                if manga and release.chapterNumber > manga.chapterNumber:
                    manga.update(release)
        
        if ircMessages:
            self.saveToFile()
        return ircMessages
"""