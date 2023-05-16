import json
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, Resource
from services import do_youtube_sentiment_analysis_of_content

app = Flask(__name__)
CORS(app)
api = Api(app)

# I need a decorator to make endpoint trace IP address


class YoutubeSentimentAnalysis(Resource):
    def get(self, url):
        """Only API endpoint for now, make a get request with a youtube content url

        Returns:
            JSON: list of comments with sentiment analysis scores
        """

        """
        print("> Request remote_addr : ", request.remote_addr)
        print("> Request remote_addr_2 : {}".format(request.environ["REMOTE_ADDR"]))
        print("> Request remote_port : {}".format(request.environ["REMOTE_PORT"]))
        """

        if url == "" or url == None:
            print("Please provide content url, exiting program...")
            error_json = json.dumps({"error": "Please provide content url"})
            return error_json
        print("url123123 : ", url)  # delete this later
        stats, comments = do_youtube_sentiment_analysis_of_content(
            youtube_content_url=url
        )
        response_dict = {"stats": stats, "comments": comments}
        return json.dumps(response_dict)


api.add_resource(YoutubeSentimentAnalysis, "/<string:url>")

if __name__ == "__main__":
    app.run(debug=True)
