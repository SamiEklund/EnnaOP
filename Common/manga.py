""" Manga package """

from Common.chapter import Chapter

class Manga(object):
    """ Class for manga information """
    name = None
    chapter = None
    followers = None

    def __init__(self, name, chapter=None, followers=None):
        self.name = name
        self.chapter = chapter
        if not self.chapter:
            self.chapter = Chapter(0, "No link available!")
        self.followers = followers
        if not self.followers:
            self.followers = []

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
        if self.chapter.number.is_integer():
            chapter_number = int(self.chapter.number)
        else:
            chapter_number = self.chapter.number

        release_message = self.name + " " + str(chapter_number) + " is out!"
        release_message += " " + " ".join(self.followers)
        release_message += "\n" + self.chapter.link
        return  release_message

    def update_chapter(self, chapter):
        """ Update chapter information based on manga object """
        if self.chapter.is_new_release(chapter):
            self.chapter = chapter
            return True
        return False
