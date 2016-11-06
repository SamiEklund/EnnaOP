# EnnaOP

EnnaOP is an IRC bot that monitors different manga scan sites for new manga releases. EnnaOP is currently in development.

##Commands
All commands sent to EnnaOP must mention her nickname at the beginning of the line. Enna_OP scans the whole message for commands so you may add additional words to the command if you wish.   
For example:  
> Enna_OP: subscribe me to One Piece  
> Enna_OP: subscribe One Piece

####List of current commands
Command | Syntax | Description
--------|--------|------------
Subscribe | subscribe manga name | Adds commanding user to that mangas followers list. 
Unsubscribe | unsubscribe manga name | Removes commanding user from mentioned mangas followers list. 

##Data
EnnaOP reads current releases from file in JSON format. Each manga is its own JSON object and the mangas are separated with linebreaks.

####JSON object example
```JSON
{
    "py/object": "annaop.Manga",
    "publishedDate": "Thu, 27 Oct 2016 7:47:01 -0700",
    "chapterNumber": 844,
    "mangaName": "One Piece",
    "followers": ["List", "of", "nicknames", "to", "notify", "on", "release"],
    "chapterLink": "http://linkto.the/latest/chapter",
    "chapterTitle": "Luffy vs Sanji"
}
```
