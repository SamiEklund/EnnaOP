# -*- coding: utf-8 -*-
import feedparser, jsonpickle

class Manga:
    def __init__(self, mangaName, chapterNumber, chapterTitle, chapterLink, publishedDate):
        self.mangaName = mangaName
        self.chapterNumber = chapterNumber
        self.chapterTitle = chapterTitle
        self.publishedDate = publishedDate
        self.chapterLink = chapterLink
        self.followers = []

    def setFollowers(self, followers):
        self.followers = followers

    def addFollower(self, follower):
        self.followers += follower

    def toString(self):
        return self.name + " No. " + str(self.chapterNumber) + " - " + self.chapterTitle + " | " + self.publishedDate

    def getMessage(self):
        return [self.mangaName + " " + str(self.chapterNumber) + " is out! " + " ".join(self.followers), self.chapterLink]

class MangaParser:
    mangaList = None
    mangaFile = "manga.txt"

    def __init__(self):
        self.loadFromFile()
        releases = self.checkForNewReleases(self.parseMangaStream())
        for msg in releases:
            print(msg[0] + "\n" + msg[1])

    def parseMangaStream(self):
        feed = feedparser.parse("http://mangastream.com/rss")
        items = feed["items"]
        feedMangas = []

        for item in items:
            chapterTitle = item.description
            publishedDate = item.published
            chapterLink = item.link
            chapterNumber = None
            mangaName = None

            # Get chapter number and manga name from title
            title = item.title
            titleInParts = title.split(" ")
            chapterNumber = titleInParts[len(titleInParts)-1]
            del titleInParts[len(titleInParts)-1]
            mangaName = " ".join(titleInParts)

            try:
                chapterNumber = int(chapterNumber)
            except:
                continue

            feedMangas.append(Manga(mangaName, chapterNumber, chapterTitle, chapterLink, publishedDate))
        return feedMangas

    def checkForNewReleases(self, releases):
        newReleases = []
        ircMessages = []

        for release in releases:
            try:
                manga = self.mangaList[release.mangaName]
            except:
                continue
            if release.chapterNumber > manga.chapterNumber:
                newReleases.append(release)

        for release in newReleases:
            manga = self.mangaList[release.mangaName]
            ircMessages.append(release.getMessage())
            if manga and release.chapterNumber > manga.chapterNumber:
                self.mangaList[release.mangaName] = release
        
        self.saveToFile()
        return ircMessages
        

    def saveToFile(self):
        file = open(self.mangaFile, "w")
        for manga in self.mangaList:
            file.write(jsonpickle.encode(self.mangaList[manga]) + "\n")
        file.close()

    def loadFromFile(self):
        self.mangaList = {}
        file = open(self.mangaFile, "r")
        for line in file:
            manga = jsonpickle.decode(line)
            self.mangaList[manga.mangaName] = manga
        file.close()


MangaParser()
