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
    
TODO : Update this text with new classes
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


class YoutubeOfficialAPIWrapper:
    """_summary_"""

    @classmethod
    def parse_single_comment(cls, comment):
        item = comment

        video_id = item["snippet"]["videoId"]
        comment_youtube_id = item["snippet"]["topLevelComment"]["id"]
        total_reply_count = item["snippet"]["totalReplyCount"]
        text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        published_at = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
        like_count = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
        author_name = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        author_channel_id = item["snippet"]["topLevelComment"]["snippet"][
            "authorChannelId"
        ]["value"]
        author_profile_image_url = item["snippet"]["topLevelComment"]["snippet"][
            "authorProfileImageUrl"
        ]
        comment_dict = {
            "video_id": video_id,
            "comment_youtube_id": comment_youtube_id,
            "total_reply_count": total_reply_count,
            "text": text,
            "published_at": published_at,
            "like_count": like_count,
            "author_name": author_name,
            "author_channel_id": author_channel_id,
            "author_profile_image_url": author_profile_image_url,
        }
        return comment_dict

    @classmethod
    def get_comments(cls, video_code):
        """Returns a list of comments for a given video code"""
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError

        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = "AIzaSyBfy8cU5_1496l3nejtIAJc9JiBm2C9JLQ"
        youtube = build(api_service_name, api_version, developerKey=DEVELOPER_KEY)
        try:
            response = (
                youtube.commentThreads()
                .list(
                    part="snippet",
                    maxResults=100,
                    textFormat="plainText",
                    videoId=video_code,
                )
                .execute()
            )
        except HttpError as e:
            print("HttpError at video (not found): {}".format(e))
            return

        return_list = []

        for item in response["items"]:
            try:
                item = cls.parse_single_comment(item)
                return_list.append(item)
            except KeyError as e:
                print("KeyError at  {} \nerr msg: {}".format(video_code, e))
                print("IntegrityError at  {} \nerr msg: {}".format(video_code, e))

        return return_list


class OpenAIAPIWrapper:
    @classmethod
    def generate_prompt(cls):
        return """I will give you a list of YouTube video comments with their ids, I want you to perform these actions on each one:

        - Classify the sentiment in the comment (negative, neutral, positive),
        - Calculate an sentiment score between [-100, 100] (-100 negative, 0 neutral, +100 positive)

        * Your response must be in the same schame as the sample response below 
        * Your response should be a single line of valid JSON, please remove all whitespace from your response

        Here is a sample response:

        { "comments" = [ { "code": "comment_1_code", "sentiment": "positive", "score": "+90", }, { "code": "comment_2_code", "sentiment": "positive", "score": "+90", }, { "code": "comment_3_code", "sentiment": "positive", "score": "+90", }] }

        Good luck!
        """

    @classmethod
    def parse_response(cls, response):
        import json

        response_text = response["choices"][0]["message"]["content"]
        response_json = json.loads(response_text)
        comments = response_json["comments"]
        for c in comments:
            print(c["code"], c["sentiment"], c["score"])
        return comments

    @classmethod
    def make_request(cls, comments):
        import os
        import openai
        from dotenv import load_dotenv

        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

        model = "gpt-3.5-turbo"
        prompt = cls.generate_prompt()
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": "Okay, let's go!"},
                {"role": "user", "content": str(comments)},
            ],
            temperature=0,
        )

        return cls.parse_response(response)


class SubtitleManager:
    """_summary_"""

    def __init__(self):
        print("called __init__ at SubtitleManager")

    @classmethod
    def get_subtitles(cls, video_id):
        """_summary_

        Args:
            video_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        print("called parse at SubtitleManager")

        if video_id == "" or video_id == None:
            print("Please provide video_id")
            exit()

        from youtube_transcript_api import YouTubeTranscriptApi

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
        except Exception as e:
            print("Exception at video (not found): {}".format(e))
            return

        return_list = []
        for item in transcript:
            return_list.append(item["text"])

        print("reutrn2727", return_list)
        return return_list
