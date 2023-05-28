def process_youtube_api_response(raw_comment: dict, add_translation=True) -> dict:
    """Processes a single raw comment from the youtube api response (sets the keys to the values we want)

    Args:
        raw_comment (dict): raw api response for a single comment

    Returns:
        dict: processesed comment (with keys we want)
    """
    text_translated = ""
    if add_translation:
        from models import TextTranslator

        text_translated = TextTranslator.to_english(raw_comment["content"])

    comment = {
        "user_pk": raw_comment["author"]["id"],
        "username": raw_comment["author"]["name"],
        "profile_pic_url": raw_comment["author"]["thumbnails"][0]["url"],
        "like_count": raw_comment["votes"]["simpleText"],
        "reply_count": raw_comment["replyCount"],
        "text": raw_comment["content"],
        "text_translated": text_translated,
        "created_at": raw_comment["published"],
    }
    return comment


def do_youtube_sentiment_analysis_of_content(video_code):
    from models import (
        YoutubeCommentScraper,
        TextTranslator,
        SentimentAnalysis,
        CSVExporter,
    )
    from helpers import printify

    if video_code == "" or video_code == None:
        print("Please provide video_code param, exiting program...")
        exit()

    raw_comments = YoutubeCommentScraper.get_comments(video_code)
    processed_comments = [process_youtube_api_response(c) for c in raw_comments]
    sentiment_stats = [SentimentAnalysis.analyze(c["text"]) for c in processed_comments]
    sentiment_stats_en = [
        SentimentAnalysis.analyze(c["text_translated"]) for c in processed_comments
    ]

    for c in processed_comments:
        c["stats"] = sentiment_stats[processed_comments.index(c)]
        c["stats_en"] = sentiment_stats_en[processed_comments.index(c)]

    csv_exporter = CSVExporter()
    csv_exporter.export(processed_comments)

    # Define defaults
    c_len = 0
    avr_polarity = 0
    avr_subjectivity = 0
    avr_afinn_score = 0
    avr_polarity_en = 0
    avr_subjectivity_en = 0
    avr_afinn_score_en = 0
    avr_likes, total_likes = 0, 0
    avr_replies, total_replies = 0, 0

    c_len = len(processed_comments)
    avr_polarity = (
        float(sum(c["stats"]["polarity"] for c in processed_comments)) / c_len
    )
    avr_subjectivity = (
        float(sum(c["stats"]["subjectivity"] for c in processed_comments)) / c_len
    )
    avr_afinn_score = (
        float(sum(c["stats"]["afinn"] for c in processed_comments)) / c_len
    )
    avr_polarity_en = (
        float(sum(c["stats_en"]["polarity"] for c in processed_comments)) / c_len
    )
    avr_subjectivity_en = (
        float(sum(c["stats_en"]["subjectivity"] for c in processed_comments)) / c_len
    )
    avr_afinn_score_en = (
        float(sum(c["stats_en"]["afinn"] for c in processed_comments)) / c_len
    )

    # Calculate total likes
    for c in processed_comments:
        try:
            total_likes += c["like_count"]
        except TypeError:
            total_likes += 0

    # Calculate total replies
    for c in processed_comments:
        try:
            total_replies += c["reply_count"]
        except TypeError:
            total_replies += 0

    # Calculate average likes and replies
    avr_likes = float(total_likes) / c_len
    avr_replies = float(total_replies) / c_len

    stats = {
        "total_comments": c_len,
        "total_likes": total_likes,
        "total_replies": total_replies,
        "avr_polarity": avr_polarity,
        "avr_subjectivity": avr_subjectivity,
        "avr_afinn_score": avr_afinn_score,
        "avr_polarity_en": avr_polarity_en,
        "avr_subjectivity_en": avr_subjectivity_en,
        "avr_afinn_score_en": avr_afinn_score_en,
        "avr_likes": avr_likes,
        "avr_replies": avr_replies,
    }

    print("completed main.py successfully")
    return stats, processed_comments


# TODO : Create a base class for other services, and inherit from it


class YoutubeCommentSentimentAnalysis:
    """This class is for Youtube Comment Sentiment Analysis Service"""

    def __init__(self, video_code):
        if video_code == "" or video_code == None:
            print("Please provide video code, exiting program...")
            exit()
        self.video_code = video_code

    def start(self):
        stats, comments = do_youtube_sentiment_analysis_of_content(self.video_code)
        return stats, comments
