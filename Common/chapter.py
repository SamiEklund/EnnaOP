""" Module for chapter data class """

class Chapter(object):
    """ Class for storing chapter data """
    number = None
    link = None
    title = None
    publish_date = None

    def __init__(self, number, link, title=None, publish_date=None):
        self.number = number
        self.link = link
        self.title = title
        self.date = publish_date

    def is_new_release(self, chapter):
        """ Checks if given chapter is new release compared this chapter """
        if not chapter:
            return False

        return chapter.number > self.number
