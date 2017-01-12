""" Manga package """

from chapter import Chapter

class Manga(object):
    """ Class for manga information """
    name = None
    chapter = None
    followers = None

    def __init__(self, name, chapter=None, followers=None):
        self.name = name
        self.chapter = chapter
        if not chapter:
            self.chapter = Chapter(0, "No link available!")
        self.followers = followers
        if not followers:
            followers = []

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
        release_message = self.name + " " + str(self.chapter.number) + " is out!"
        release_message += " " + " ".join(self.followers)
        release_message += "\n" + self.chapter.link
        return  release_message

    def update_chapter(self, chapter):
        """ Update chapter information based on manga object """
        if self.chapter.is_new_release(chapter):
            self.chapter = chapter
