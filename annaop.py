import feedparser

# TODO At startup load current manga chapters from file

mangaStatuses = {"One Piece": "EMPTY", "Hajime No Ippo": "EMPTY"}

def checkMangastream():
   rss_url = "http://mangastream.com/rss"
   feed = feedparser.parse(rss_url)
   items = feed["items"]
   for item in items:
       title = item["title"]
       for manga in mangaStatuses:
            if manga.lower() in title.lower():
                print "We follow this manga! Last chapter was: " + mangaStatuses[manga]
                if mangaStatuses[manga].lower() is title.lower():
                    print title + " is out! Doublecaster Anna_OP"
                    mangaStatuses[manga] = title
                else:
                    print "This wasn't a new release..."

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

loadMangaStatuses()
checkMangastream()
saveMangaStatuses()
