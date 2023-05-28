import json
from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource
from services import YoutubeCommentSentimentAnalysis

# frontend-reactjs/
app = Flask(
    __name__,
    # static_folder="/../frontend-reactjs/build/",
    static_folder="../frontend-reactjs/build/",
    # static_folder="frontend-reactjs/build/",
    static_url_path="/",
    # template_folder="../build/",
)
CORS(app)
api = Api(app)

# TODO I need a decorator to make endpoint trace IP address


# This is the entry endpoint for the React App
@app.route("/")
def serve():
    print("serving index.html (hope you didn't forget to run 'npm run build')")
    try:
        return app.send_static_file("index.html")
    except Exception as e:
        error_string = "Error serving index.html : {}".format(e)
        print(error_string)
        return error_string


class YoutubeSentimentAnalysis(Resource):
    def get(self, video_code):
        """Only API endpoint for now, make a get request with a youtube content url

        Returns:
            JSON: list of comments with sentiment analysis scores
        """

        """
        print("> Request remote_addr : ", request.remote_addr)
        print("> Request remote_addr_2 : {}".format(request.environ["REMOTE_ADDR"]))
        print("> Request remote_port : {}".format(request.environ["REMOTE_PORT"]))
        """

        print("video code submitted to flask api : ", video_code)  # delete this later

        if video_code == "" or video_code == None:
            print("Please provide content url, exiting program...")
            error_json = json.dumps({"error": "Please provide content url"})
            return error_json
        stats, comments = YoutubeCommentSentimentAnalysis(video_code=video_code).start()
        response_dict = {"stats": stats, "comments": comments}
        return json.dumps(response_dict)


api.add_resource(YoutubeSentimentAnalysis, "/api/<string:video_code>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
