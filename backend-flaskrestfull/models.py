from abc import ABC, abstractmethod

from attr import dataclass
from typing import Optional

# TODO : Add docstrings to all methods
# TODO : Add type hints to all methods (take a look at pydantic)
# TODO : Seperate scraping & parsing logic to different classes
# TODO : Scraping and parsing must have their own base classes


@dataclass
class CommentGPTStats:
    """_summary_"""

    code: str
    sentiment: str
    score: int

    def to_json(self):
        return {
            "code": self.code,
            "sentiment": self.sentiment,
            "score": self.score,
        }

    def from_json(self, json):
        return CommentGPTStats(**json)

    def to_dict(self):
        return {
            "code": self.code,
            "sentiment": self.sentiment,
            "score": self.score,
        }

    def from_dict(self, dict):
        return CommentGPTStats(**dict)


@dataclass
class CommentPSAStats:
    """_summary_"""

    polarity: float
    subjectivity: float
    afinn: float

    def to_json(self):
        return {
            "polarity": self.polarity,
            "subjectivity": self.subjectivity,
            "afinn": self.afinn,
        }

    def to_dict(self):
        return {
            "polarity": self.polarity,
            "subjectivity": self.subjectivity,
            "afinn": self.afinn,
        }


@dataclass
class Comment:
    """_summary_"""

    comment_youtube_id: str
    text: str
    published_at: str
    like_count: int
    author_name: str
    author_channel_id: str
    author_profile_image_url: str
    total_reply_count: int

    def to_json(self):
        return {
            "comment_youtube_id": self.comment_youtube_id,
            "text": self.text,
            "published_at": self.published_at,
            "like_count": self.like_count,
            "author_name": self.author_name,
            "author_channel_id": self.author_channel_id,
            "author_profile_image_url": self.author_profile_image_url,
            "total_reply_count": self.total_reply_count,
        }

    def to_dict(self):
        return {
            "comment_youtube_id": self.comment_youtube_id,
            "text": self.text,
            "published_at": self.published_at,
            "like_count": self.like_count,
            "author_name": self.author_name,
            "author_channel_id": self.author_channel_id,
            "author_profile_image_url": self.author_profile_image_url,
            "total_reply_count": self.total_reply_count,
        }


class BaseYoutubeCommentScraper(ABC):
    """Abstract Base Class for other concrete YoutubeCommentScraper classes.
    Official Youtube API scraper and 3rd party scraper classes will inherit from this class.
    """

    @abstractmethod
    def parse_single_comment(self, comment: dict) -> dict:
        """

        Args:
            comment (dict): a single comment dictionary from api response

        Returns:
            _type_: _description_
        """
        pass

    @abstractmethod
    def parse_comment_list(self, comment_list: list[dict]) -> list[dict]:
        pass

    @abstractmethod
    def get_comments(self, content_code: str) -> list[dict]:
        """_summary_

        Args:
            content_url (_type_): _description_

        Returns:
            _type_: _description_
        """
        pass


class YoutubeThirdPartyCommentScraper(BaseYoutubeCommentScraper):
    @classmethod
    def parse_single_comment(cls, comment: dict) -> dict:
        print("\n parsing 3rd party api comment: ", comment)
        comment_youtube_id = comment["id"]
        total_reply_count = comment["replyCount"]
        text = comment["content"]
        published_at = comment["published"]
        like_count = comment["votes"]["simpleText"]
        author_name = comment["author"]["name"]
        author_channel_id = comment["author"]["id"]
        author_profile_image_url = comment["author"]["thumbnails"][0]["url"]

        parsed_comment = {
            "comment_youtube_id": comment_youtube_id,
            "total_reply_count": total_reply_count,
            "text": text,
            "published_at": published_at,
            "like_count": like_count,
            "author_name": author_name,
            "author_channel_id": author_channel_id,
            "author_profile_image_url": author_profile_image_url,
        }

        return parsed_comment

    @classmethod
    def parse_comment_list(cls, comment_list: list[dict]) -> list[dict]:
        return [cls.parse_single_comment(c) for c in comment_list]

    @classmethod
    def get_comments(cls, video_code: str) -> list[dict]:
        """Returns a list of comments for a given video code"""
        print("called get_comments at YoutubeThirdPartyCommentScraper")
        from youtubesearchpython import Comments

        comments = Comments(video_code)
        while comments.hasMoreComments:
            comments.getNextComments()

        return comments.comments["result"]


class YoutubeOfficialAPICommentScraper(BaseYoutubeCommentScraper):
    @classmethod
    def parse_single_comment(cls, comment: dict) -> Comment:
        print("\n parsing official api comment: ", comment)
        comment_youtube_id = comment["snippet"]["topLevelComment"]["id"]
        total_reply_count = comment["snippet"]["totalReplyCount"]
        text = comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        published_at = comment["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
        like_count = comment["snippet"]["topLevelComment"]["snippet"]["likeCount"]
        author_name = comment["snippet"]["topLevelComment"]["snippet"][
            "authorDisplayName"
        ]
        author_channel_id = comment["snippet"]["topLevelComment"]["snippet"][
            "authorChannelId"
        ]["value"]
        author_profile_image_url = comment["snippet"]["topLevelComment"]["snippet"][
            "authorProfileImageUrl"
        ]

        parsed_comment = Comment(
            comment_youtube_id=comment_youtube_id,
            text=text,
            published_at=published_at,
            like_count=like_count,
            total_reply_count=total_reply_count,
            author_name=author_name,
            author_channel_id=author_channel_id,
            author_profile_image_url=author_profile_image_url,
        )
        return parsed_comment

    @classmethod
    def parse_comment_list(cls, comment_list: list[dict]) -> list[Comment]:
        return [cls.parse_single_comment(c) for c in comment_list]

    @classmethod
    def get_comments(cls, video_code: str) -> list[dict]:
        """Returns a list of comments for a given video code"""
        print("called get_comments at YoutubeOfficialAPICommentScraper")
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

        return response["items"]


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

        Returns:x
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
    def analyze_psa(cls, text):
        polarity, subjectivity = cls.analyze_textblob(text)
        afinn = cls.analyze_afinn(text)

        comment_psa_stats = CommentPSAStats(
            polarity=polarity, subjectivity=subjectivity, afinn=afinn
        )

        return comment_psa_stats


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
    def parse_response(cls, response) -> list[CommentGPTStats]:
        import json

        response_text = response["choices"][0]["message"]["content"]
        response_json = json.loads(response_text)
        comments = response_json["comments"]
        for c in comments:
            print(c["code"], c["sentiment"], c["score"])
        # TODO
        comments = [
            CommentGPTStats(code=c["code"], sentiment=c["sentiment"], score=c["score"])
            for c in comments
        ]
        return comments

    @classmethod
    def make_request(cls, comments) -> list[CommentGPTStats]:
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
            temperature=0.20,
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
