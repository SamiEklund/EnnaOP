import feedparser, json

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

    def toJSON(self):
        return json.dumps(self.__dict__, sort_keys = True)

class MangaParser:
    mangaList = None
    mangaFile = "manga.txt"

    def __init__(self):
        # self.mangaList = self.parseMangaStream()
        # self.loadFromFile()
        # for manga in self.mangaList:
        #    print(manga)
        # self.saveToFile()

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
                print("Entry " + mangaName + " has no chapter number! Skipping it!")
                continue

            feedMangas.append(Manga(mangaName, chapterNumber, chapterTitle, chapterLink, publishedDate))
        return feedMangas

    def saveToFile(self):
        file = open(self.mangaFile, "w")
        for manga in self.mangaList:
            file.write(manga.toJSON() + "\n")
        file.close()

    def loadFromFile(self):
        self.mangaList = []
        file = open(self.mangaFile, "r")
        for line in file:
            self.mangaList += json.loads(line)

        file.close()


MangaParser()