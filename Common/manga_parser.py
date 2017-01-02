""" """

import json
import jsonpickle

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
            if manga.mangaName.lower() == manga_title.lower():
                return manga
        return None

    @staticmethod
    def add_follower_to_manga(manga_title, user):
        """ Adds user to mangas follower list  """
        manga = MangaParser.get_manga_by_title(manga_title)
        if manga and manga.addFollower(user):
            MangaParser.save_to_file()
            return manga.mangaName
        return None

    @staticmethod
    def remove_follower_from_manga(manga_title, user):
        """ Removes user from mangas follower list """
        manga = MangaParser.get_manga_by_title(manga_title)
        if manga and manga.removeFollower(user):
            MangaParser.save_to_file()
            return manga.mangaName
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

    def createNewManga(self, mangaName):
        manga = self.getMangaByTitle(mangaName) # FIXME: This wont work here, cant follow Dragon Ball and Dragon Ball Z
        if manga is None:
            manga = Manga(mangaName, 0, "nolinkavailable")
            self.mangaList.append(manga)
            ircMsgCount = len(self.checkForNewReleases())
            if ircMsgCount == 0:
                self.saveToFile()
            return manga.mangaName
        else:
            return None
"""