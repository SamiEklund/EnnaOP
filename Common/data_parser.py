""" Data parsing module """
import re
import feedparser
import jsonpickle
from manga import Manga
from chapter import Chapter

class DataSource(object):
    """ Data class for handling data source infomation """
    source_url = None
    data_type = None
    data_mappings = None

    def __init__(self, source_url, data_type, data_mappings):
        self.source_url = source_url
        self.data_type = data_type
        self.data_map = data_mappings

def load_data_sources():
    """ Load DataSources from a JSON file """
    source_file = open("datasources.json", "r")
    source_list = jsonpickle.decode(source_file.read())
    source_file.close()
    return source_list

class DataHandler(object):
    """ Static class for data fetching and parsing """

    @staticmethod
    def get_manga_from_rss(data_source):
        """ Parses rss based on given DataSource and returns release list """
        rss_feed = feedparser.parse(data_source.source_url)

        rss_items = rss_feed["items"]
        manga_list = []

        for item in rss_items:
            manga_data = {}
            for mapping in data_source.data_mappings:
                node_data = item[mapping["node"]]
                parse_method = mapping["method"]
                regex = mapping["regex"]
                manga_data[mapping["dataname"]] = DataHandler.parse_node(node_data, parse_method, regex)

            manga = DataHandler.create_manga(manga_data)

            if manga:
                manga_list.append(manga)

        return manga_list

    @staticmethod
    def get_manga_from_html(data_source):
        """ Get manga from HTML based on DataSource """
        raise NotImplementedError

    @staticmethod
    def parse_node(node, method, regex):
        """ Parses item from node data """
        # TODO: Remove method, if not needed
        if method == "regex":
            reg = re.compile(regex)
            regex_result = reg.search(node)
            if regex_result:
                return regex_result.group(0)
            return "REGEXFAILED"
        else:
            print "No method recognized :("

    @staticmethod
    def create_manga(data):
        """ Creates new manga object """
        manga_name = data["manganame"] if "manganame" in data else None
        chapter_link = data["chapterlink"] if "chapterlink" in data else None
        chapter_number = data["chapternumber"] if "chapternumber" in data else None

        try:
            chapter_number = float(chapter_number)
        except ValueError:
            return None

        if not manga_name or not chapter_link or not chapter_number:
            return None

        publish_date = data["publisheddate"] if "publisheddate" in data else None
        chapter_title = data["chaptertitle"] if "chaptertitle" in data else None

        chapter = Chapter(chapter_number, chapter_link, chapter_title, publish_date)

        return Manga(manga_name, chapter)

    data_sources = load_data_sources()
