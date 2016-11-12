# -*- coding: utf-8 -*-
import feedparser, jsonpickle, re, json

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
        chaptNum = int(self.chapterNumber) if self.chapterNumber.is_integer() else self.chapterNumber
        return self.name + " No. " + str(chaptNum) + " - " + self.chapterTitle + " | " + self.publishedDate

    def getMessage(self):
        chaptNum = int(self.chapterNumber) if self.chapterNumber.is_integer() else self.chapterNumber
        return self.mangaName + " " + str(chaptNum) + " is out! " + " ".join(self.followers) + "\n" + self.chapterLink

    def update(self, newManga):
        if not newManga or not newManga.chapterTitle or not newManga.chapterNumber:
            return
        self.chapterNumber = newManga.chapterNumber
        self.chapterLink = newManga.chapterLink
        self.publishedDate = newManga.publishedDate
        self.chapterTitle = newManga.chapterTitle

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

    def subscribe(self, message, user):
        manga = self.getMangaByTitle(message)
        if manga and self.mangaList[manga].addFollower(user):
            self.saveToFile()
            return manga
        return None
        
    def unsubscribe(self, message, user):
        manga = self.getMangaByTitle(message)
        if manga and self.mangaList[manga].removeFollower(user):
            self.saveToFile()
            return manga
        return None

    def getMangaByTitle(self, mangaStr):
        for manga in self.mangaList:
            if manga.mangaName.lower() in mangaStr.lower():
                return manga
        

    def saveToFile(self):
        file = open(self.mangaFile, "w")
        jsonData = jsonpickle.encode(self.mangaList)
        jsonData = json.loads(jsonData)
        json.dump(jsonData, file, indent=4, sort_keys=True,separators=(',', ':'))
        file.close()

    def loadFromFile(self):
        file = open(self.mangaFile, "r")
        self.mangaList = jsonpickle.decode(file.read())
        file.close()

    def loadSources(self):
        file = open("datasources.json", "r")
        self.sourceList = jsonpickle.decode(file.read())
        file.close()
