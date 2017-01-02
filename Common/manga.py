""" Manga package """

class Manga(object):
    """ Class for manga information """
    #TODO create issue to github about splitting manga into manga and chapter
    manga_name = None
    chapter_number = None
    chapter_link = None
    chapter_title = None
    publish_date = None
    followers = None

    def __init__(self, manga_name, chapter_number, chapter_link,
                 chapter_title=None, published_date=None):
        self.manga_name = manga_name
        self.chapter_number = chapter_number
        self.chapter_link = chapter_link
        self.chapter_title = chapter_title
        self.publish_date = published_date

    def set_followers(self, followers):
        """ Sets mangas followers """
        self.followers = followers

    def add_follower(self, user):
        """ Adds user to followers """
        if user not in self.followers:
            self.followers.append(user)
            return True
        return False

    def remove_follower(self, user):
        """ Removes user from followers """
        if user in self.followers:
            self.followers.remove(user)
            return True
        return False

    def get_release_message(self):
        """ Returns message with release information """
        release_message = self.manga_name + " " + str(self.chapter_number) + " is out!"
        release_message += " " + " ".join(self.followers)
        release_message += "\n" + self.chapter_link
        return  release_message

    def update_chapter(self, new_manga):
        """ Update chapter information based on manga object """
        if not new_manga or not new_manga.chapter_number or not new_manga.chapter_link:
            return

        self.chapter_number = new_manga.chapter_number
        self.chapter_link = new_manga.chapter_link

        if new_manga.publish_date:
            self.publish_date = new_manga.publish_date
        else:
            self.publish_date = "TODAY"

        if new_manga.chapter_title:
            self.chapter_title = new_manga.chapter_title
        else:
            self.chapter_title = None
