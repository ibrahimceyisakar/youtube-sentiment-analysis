def do_youtube_sentiment_analysis_of_content(youtube_content_url):
    from models import (
        YoutubeCommentScraper,
        TextTranslator,
        SentimentAnalysis,
        CSVExporter,
    )

    if youtube_content_url == "" or youtube_content_url == None:
        print("Please provide content url, exiting program...")
        exit()

    YOUTUBE_CONTENT_URL = youtube_content_url

    scraper = YoutubeCommentScraper()
    scraped_comments = scraper.get_comments(YOUTUBE_CONTENT_URL)
    comments = []

    for comment in scraped_comments:
        # Translate each comment to english
        comment_text_en = TextTranslator.to_english(comment["content"])
        # Analyze each comment's sentiment in src language (polarity, subjectivity, afinn_score)
        polarity, subjectivity = SentimentAnalysis.analyze(comment["content"])
        afinn_score = SentimentAnalysis.analyze_afinn(comment["content"])
        # Analyze each comment's sentiment in en language (polarity_en, subjectivity_en, afinn_score_en)
        polarity_en, subjectivity_en = SentimentAnalysis.analyze(comment_text_en)
        afinn_score_en = SentimentAnalysis.analyze_afinn(comment_text_en)

        """
        These three points are for src language: polarity, subjectivity, afinn_score 
        These three points are for en language: polarity_en, subjectivity_en, afinn_score_en
        So by comparing these couples to each other,
        we can analyse the difference between the two languages,
        and decide if the translation is good or not for SM content sentiment analysis.
        """
        comment_dict = {
            "user_pk": comment["author"]["id"],
            "username": comment["author"]["name"],
            "profile_pic_url": comment["author"]["thumbnails"][0]["url"],
            "text": comment["content"],
            "text_translated": comment_text_en,
            "created_at_utc": comment["published"],
            "like_count": comment["votes"]["simpleText"],
            "reply_count": comment["replyCount"],
            "polarity": polarity,
            "subjectivity": subjectivity,
            "afinn_score": afinn_score,
            "polarity_en": polarity_en,
            "subjectivity_en": subjectivity_en,
            "afinn_score_en": afinn_score_en,
        }
        comments.append(comment_dict)

    csv_exporter = CSVExporter()
    csv_exporter.export(comments)

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

    c_len = len(comments)
    avr_polarity = float(sum(c["polarity"] for c in comments)) / c_len
    avr_subjectivity = float(sum(c["subjectivity"] for c in comments)) / c_len
    avr_afinn_score = float(sum(c["afinn_score"] for c in comments)) / c_len
    avr_polarity_en = float(sum(c["polarity_en"] for c in comments)) / c_len
    avr_subjectivity_en = float(sum(c["subjectivity_en"] for c in comments)) / c_len
    avr_afinn_score_en = float(sum(c["afinn_score_en"] for c in comments)) / c_len

    # Calculate total likes
    for c in comments:
        try:
            total_likes += c["like_count"]
        except TypeError:
            total_likes += 0

    # Calculate total replies
    for c in comments:
        try:
            total_replies += c["reply_count"]
        except TypeError:
            total_replies += 0

    # Calculate average likes and replies
    avr_likes = float(total_likes) / c_len
    avr_replies = float(total_replies) / c_len

    """
    # Deprecated
    avr_likes = float(sum(c.get("like_count", 0) for c in comments)) / c_len
    avr_replies = float(sum(int(c.get("reply_count")) for c in comments)) / c_len
    """

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
    return stats, comments
