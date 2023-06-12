def do_youtube_sentiment_analysis_of_content(video_code):
    """Main function for doing sentiment analysis of youtube comments"""

    from models import (
        YoutubeThirdPartyCommentScraper,
        YoutubeOfficialAPICommentScraper,
        OpenAIAPIWrapper,
        # TextTranslator,
        SentimentAnalysis,
        # SubtitleManager,
        # CSVExporter,
    )

    if video_code == "" or video_code == None:
        print("Please provide video_code param, exiting program...")
        exit()

    # Get comments from Youtube Data API v3
    raw_comments = YoutubeOfficialAPICommentScraper.get_comments(video_code)

    # Below method returns a list of Comment objects
    processed_comments = YoutubeOfficialAPICommentScraper.parse_comment_list(
        raw_comments
    )

    if processed_comments == None or processed_comments == []:
        print("No comments to process, exiting program...")
        exit()

    print("Len of processed_comments: ", len(processed_comments))

    # Calculate sentiment PSA stats for each comment (subjectivity, polarity, afinn)
    # It is a list of CommentPSAStats objects
    sentiment_stats = [
        SentimentAnalysis.analyze_psa(c.text) for c in processed_comments
    ]

    # Calculate a CommentGPT stat for each comment
    # It is a list of CommentGPTStats objects
    commentgpt_stats = OpenAIAPIWrapper.make_request(
        [(c.comment_youtube_id + " - " + c.text) for c in processed_comments]
    )
    commentgpt_stats = [c.to_json() for c in commentgpt_stats]
    processed_comments = [c.__dict__ for c in processed_comments]

    for c in processed_comments:
        c["stats"] = sentiment_stats[processed_comments.index(c)]
        c["commentgpt_stats"] = commentgpt_stats[processed_comments.index(c)]
        """
        convert to dict for json serialisation
        because c is a Comment object,
        and Comment object is not json serialisable (at the moment)
        because view returns a a dict with stats, comments keys added to it
        its better to make stats a seperate dataclass later
        """

    # csv_exporter = CSVExporter()
    # csv_exporter.export(processed_comments)

    stats = {
        "my-key-123": "my-value-123",
    }

    print("completed main.py successfully")
    print("returning v78 : ", stats, processed_comments)
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
