""" """

import json
import jsonpickle

from manga import Manga

def load_manga_file():
    """ Reads saved status from JSON file """
    manga_file = open("manga.json", "r")
    manga_list = jsonpickle.decode(manga_file.read())
    manga_file.close()
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
            if manga.manga_name.lower() == manga_title.lower():
                return manga
        return None

    @staticmethod
    def add_follower_to_manga(manga_title, user):
        """ Adds user to mangas follower list  """
        manga = MangaParser.get_manga_by_title(manga_title)
        if manga and manga.add_follower(user):
            MangaParser.save_to_file()
            return True
        return False

    @staticmethod
    def remove_follower_from_manga(manga_title, user):
        """ Removes user from mangas follower list """
        manga = MangaParser.get_manga_by_title(manga_title)
        if manga and manga.remove_follower(user):
            MangaParser.save_to_file()
            return True
        return False

    @staticmethod
    def monitor_new_manga(manga_title):
        """ Add new manga to the monitored mangas """
        manga = MangaParser.get_manga_by_title(manga_title)
        if manga is None:
            new_manga = Manga(manga_title, 0, "nolinkavailable")
            MangaParser.manga_list.append(new_manga)
            MangaParser.save_to_file()
            return True

        return False

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