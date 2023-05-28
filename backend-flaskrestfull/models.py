"""
This file contains all the core models (classes) used in the project

Classes:
    InstagramCommentScraper     (login credentials required)
    YoutubeCommentScraper       (no credentials required)
    TextTranslator              (no credentials required)    
    SentimentAnalysis           (no credentials required)
    CSVExporter                 (no credentials required)
    
Used Packages/Modules:
    https://github.com/adw0rd/instagrapi                    for InstagramCommentScraper
    https://github.com/alexmercerind/youtube-search-python  for YoutubeCommentScraper
    https://github.com/nidhaloff/deep-translator            for TextTranslator
    https://github.com/sloria/TextBlob                      for SentimentAnalysis
    https://github.com/fnielsen/afinn                       for SentimentAnalysis
"""


class InstagramCommentScraper:
    """_summary_

    Args:
        BaseCommentScraper (_type_): _description_
    """

    def __init__(self, username, password):
        print("called __init__ at InstagramCommentScraper")

        if username == "" or password == "" or username == None or password == None:
            print("Please provide username and password")
            exit()

        self.username = username
        self.password = password
        super().__init__()

    def get_comments(self, content_url):
        """This method uses instagrapi

        Args:
            content_url (_type_): _description_

        Returns:
            _type_: _description_

        # TODO: Move login to __init__ method
        """
        print("called get_comments at InstagramCommentScraper")

        if content_url == "" or content_url == None:
            print("Please provide content url")
            exit()

        if (
            self.username == ""
            or self.password == ""
            or self.username == None
            or self.password == None
        ):
            print("Please provide username and password")
            exit()

        from instagrapi import Client

        USERNAME = self.username
        PASSWORD = self.password
        CONTENT_URL = content_url

        cl = Client()
        cl.login(USERNAME, PASSWORD)

        # Get media id by post url
        media_id = cl.media_id(cl.media_pk_from_url(CONTENT_URL))

        # Get all comments
        comments = cl.media_comments(media_id, amount=0)
        print("Total comments in get_comments: ", len(comments))
        return comments


class YoutubeCommentScraper:
    @classmethod
    def get_comments(cls, content_url):
        from youtubesearchpython import Comments

        comments = Comments(content_url)
        while comments.hasMoreComments:
            comments.getNextComments()

        return comments.comments["result"]


class TextTranslator:
    """
    https://pypi.org/project/googletrans/

    Returns:
        string: translated text (or comment) in english
    """

    @classmethod
    def to_english(cls, text):
        if text == "" or text == None:
            print("Please provide text to translate")
            # exit()
            return
        from deep_translator import GoogleTranslator

        translator = GoogleTranslator(source="auto", target="en")
        translated = translator.translate(text)
        return translated


class SentimentAnalysis:
    """To do sentiment analysis on a text (or comment)
    create an instance of this class with comment_text param provided

    This class uses packages below \n
    https://github.com/ultrafunkamsterdam/googletranslate \n
    https://github.com/sloria/TextBlob \n
    https://github.com/fnielsen/afinn \n


    Args:
        text (string): target text (or comment) to do sentiment analysis on
    Returns:
        _type_: _description_
    """

    @classmethod
    def analyze_textblob(cls, text):
        """_summary_

        Args:
            text (string): target text (or comment) to do sentiment analysis on

        Returns:

            Tuple : (polarity, subjectivity)
        """
        if text == "" or text == None:
            print("Please provide text to analyze")
            # exit()
            return 0, 0

        from textblob import TextBlob

        blob = TextBlob(text)
        return blob.sentiment.polarity, blob.sentiment.subjectivity

    @classmethod
    def analyze_afinn(cls, text):
        """Alternative sentiment analysis method using Afinn

        Args:
            text (string): target text (or comment) to do sentiment analysis on

        Returns:
            int: afinn score
        """
        if text == "" or text == None:
            print("Please provide text to analyze")
            return 0

        from afinn import Afinn

        afinn = Afinn()
        return afinn.score(text)

    @classmethod
    def analyze(cls, text):
        polarity, subjectivity = cls.analyze_textblob(text)
        afinn = cls.analyze_afinn(text)
        stats = {
            "polarity": polarity,
            "subjectivity": subjectivity,
            "afinn": afinn,
        }
        return stats


class CSVExporter:
    """
    This class is responsible for exporting the comments to a CSV file
    Comments are stored in a list of dictionaries
    """

    def __init__(self):
        print("called __init__ at CSVExport")

    def export(self, comments):
        if comments == None or comments == []:
            print("No comments to export")
            return

        import csv

        keys = comments[0].keys()

        with open("comments.csv", "w", newline="") as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(comments)
