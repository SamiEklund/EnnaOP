import feedparser

def saveMangaStatuses():
    file = open("mangalog.txt", "w")
    for manga in mangaStatuses:
        file.write(manga + ";" + mangaStatuses[manga] + "\n")
    file.close()

def loadMangaStatuses():
    file = open("mangalog.txt", "r")
    for line in file:
        splitLine = line.split(";")
        mangaStatuses[splitLine[0]] = splitLine[1]
    file.close() 

class Manga:
    def __init__(self, name, chapterNumber, chapterTitle, chapterLink, publishedDate):
        self.name = name
        self.chapterNumber = chapterNumber
        self.chapterTitle = chapterTitle
        self.publishedDate = publishedDate
        self.chapterLink = chapterLink

    def toString(self):
        return self.name + " No. " + str(self.chapterNumber) + " - " + self.chapterTitle + " | " + self.publishedDate

class MangaParser:
    mangaList = None

    def __init__(self):
        mangas = self.parseMangastream()
        for manga in mangas:
            print(manga.toString())

    def parseMangastream(self):
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

MangaParser()