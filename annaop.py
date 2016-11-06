# -*- coding: utf-8 -*-
import feedparser, jsonpickle, re

class Manga:
    def __init__(self, mangaName, chapterNumber, chapterLink, chapterTitle=None, publishedDate=None, followers=None):
        self.mangaName = mangaName
        self.chapterNumber = chapterNumber
        self.chapterTitle = chapterTitle
        self.publishedDate = publishedDate
        self.chapterLink = chapterLink
        self.followers = followers

    def setFollowers(self, followers):
        self.followers = followers

    def addFollower(self, follower):
        if follower not in self.followers:
            self.followers.append(follower)
            return True
        return False

    def removeFollower(self, follower):
        if follower in self.followers:
            self.followers.remove(follower)
            return True
        return False

    def toString(self):
        return self.name + " No. " + str(self.chapterNumber) + " - " + self.chapterTitle + " | " + self.publishedDate

    def getMessage(self):
        return self.mangaName + " " + str(self.chapterNumber) + " is out! " + " ".join(self.followers) + "\n" + self.chapterLink

class DataSource:
    def __init__(self, source, type, dataMap):
        self.source = source
        self.type = type
        self.dataMap = dataMap

    def getManga(self):
        if self.type == "rss":
            data = feedparser.parse(self.source)
            parsedData = self.parseRSS(data)
            return parsedData
        elif self.type == "HTML":
            print "HTML Parsing not implemented yet"
            return None

    def parseRSS(self, rss):
        if not rss:
            return
        items = rss["items"]
        releaseList = []
        for item in items:
            mangaValues = {}
            for mapping in self.dataMap:
                mangaValues[mapping["dataname"]] = self.parseItem(item[mapping["node"]], mapping["method"], mapping["regex"])

            manga = self.createManga(mangaValues)
            if manga:
                 releaseList.append(manga)

        return releaseList

    def parseItem(self, node, method, regex):
        if method == "regex":
            reg = re.compile(regex)
            r =  reg.search(node)
            if r:
                return r.group(0)
            return "REGEXFAILED"
        else:
            print "No method recognized :("

    def createManga(self, data):
        mangaName = data["manganame"] if "manganame" in data else None
        chapterLink = data["chapterlink"] if "chapterlink" in data else None
        chapterNumber = data["chapternumber"] if "chapternumber" in data else None
        try:
            chapterNumber = float(chapterNumber)
        except:
            return None

        if mangaName is None or chapterLink is None or chapterNumber is None:
            return None
        
        publishedDate = data["publisheddate"] if "publisheddate" in data else None
        chapterTitle = data["chaptertitle"] if "chaptertitle" in data else None

        return Manga(mangaName, chapterNumber, chapterLink, chapterTitle, publishedDate)

class MangaParser:
    mangaList = None
    mangaFile = "manga.txt"
    sourceList = None

    def __init__(self):
        self.loadFromFile()
        self.loadSources()

    def checkForNewReleases(self):
        ircMessages = []

        for source in self.sourceList:
            newReleases = []
            releases = source.getManga()
            if not releases:
                continue
            for release in releases:
                try:
                    manga = self.mangaList[release.mangaName]
                except:
                    continue
                if release.chapterNumber > manga.chapterNumber:
                    release.setFollowers(manga.followers)
                    newReleases.append(release)

            for release in newReleases:
                manga = self.mangaList[release.mangaName]
                ircMessages.append(release.getMessage())
                if manga and release.chapterNumber > manga.chapterNumber:
                    self.mangaList[release.mangaName] = release
        
        if ircMessages:
            self.saveToFile()
        return ircMessages

    def subscribe(self, message, user):
        for manga in self.mangaList:
            if manga.lower() in message:
                if self.mangaList[manga].addFollower(user):
                    self.saveToFile()
                    return manga
        return None
        
    def unsubscribe(self, message, user):
        for manga in self.mangaList:
            if manga.lower() in message:
                if self.mangaList[manga].removeFollower(user):
                    self.saveToFile()
                    return manga
        return None

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

    def loadSources(self):
        file = open("datasources.json", "r")
        self.sourceList = jsonpickle.decode(file.readline())
        file.close()
