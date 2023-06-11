def process_youtube_api_response(raw_comment: dict, add_translation=False) -> dict:
    """Processes a single raw comment from the 3rd party youtube api response (sets the keys to the values we want)

    Args:
        raw_comment (dict): raw api response for a single comment
        add_translation (bool, optional): whether to add translation to the comment. Defaults to False.

    Returns:
        dict: processesed comment (with keys we want)
    """
    text_translated = ""
    if add_translation:
        from models import TextTranslator

        text_translated = TextTranslator.to_english(raw_comment["content"])

    comment = {
        "user_pk": raw_comment["author_channel_id"],
        "username": raw_comment["author_name"],
        "profile_pic_url": raw_comment["author_profile_image_url"],
        "like_count": raw_comment["like_count"],
        "reply_count": raw_comment["total_reply_count"],
        "text": raw_comment["text"],
        "text_translated": text_translated,
        "created_at": raw_comment["published_at"],
    }
    return comment


def do_youtube_sentiment_analysis_of_content(video_code):
    from models import (
        # YoutubeCommentScraper,    # 3rd party API for getting youtube comments
        YoutubeOfficialAPIWrapper,  # Official Youtube API for getting youtube comments
        OpenAIAPIWrapper,  # OpenAI API for classifying and scoring comments
        # TextTranslator,           # For translating text to english (no longer used)
        SentimentAnalysis,  # For calculating sentiment stats (polarity, subjectivity, afinn)
        # SubtitleManager,  # For getting subtitles (by 3rd party API)
        CSVExporter,  # For exporting comments to CSV file
    )

    if video_code == "" or video_code == None:
        print("Please provide video_code param, exiting program...")
        exit()

    # Get comments from official youtube api (or 3rd party scraper)
    # Use YoutubeCommentScraper if you don't have a youtube api key
    raw_comments = YoutubeOfficialAPIWrapper.get_comments(video_code)

    # These two lines are for 3rd party scraper
    # raw_comments = YoutubeCommentScraper.get_comments(video_code)
    # processed_comments = [process_official_api_response(c) for c in raw_comments]

    processed_comments = raw_comments
    if processed_comments == None or processed_comments == []:
        print("No comments to process, exiting program...")
        exit()

    print("Len of processed_comments: ", len(processed_comments))
    COMMENT_COUNT_LIMIT = 20
    if len(processed_comments) > COMMENT_COUNT_LIMIT:
        processed_comments = processed_comments[:COMMENT_COUNT_LIMIT]

    # Calculate sentiment stats for each comment (subjectivity, polarity, afinn)
    sentiment_stats = [SentimentAnalysis.analyze(c["text"]) for c in processed_comments]

    commentgpt_stats = OpenAIAPIWrapper.make_request(
        [(c["comment_youtube_id"] + " - " + c["text"]) for c in processed_comments]
    )

    for c in processed_comments:
        c["stats"] = sentiment_stats[processed_comments.index(c)]
        c["commentgpt_stats"] = commentgpt_stats[processed_comments.index(c)]

    # csv_exporter = CSVExporter()
    # csv_exporter.export(processed_comments)

    stats = {
        "my-key-123": "my-value-123",
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
