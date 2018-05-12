from flask import Flask

app = Flask(__name__)


@app.route("/videos")
def videos():
    return "videos"

