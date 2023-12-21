import json
from flask import Flask, request, jsonify
# import cloudinary
import get_info
from video_downloader import video_download
from playlist_downloader import download_playlist
from flask_cors import CORS
from connect_table import videos
import os


app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


@app.route("/")
def main():
    return "<p>Api is working fine!</p>"


@app.route('/video/get')
def get_video():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is missing"}, 400)
    video = get_info.get_video_info(url)
    return video


@app.route('/playlist/get')
def get_playlist():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is missing"}, 400)
    playlist = get_info.get_playlist_info(url)
    print(playlist)
    return playlist


@app.route('/video/download', methods=['POST'])
def video():
    data = request.json
    try:
        url = video_download(data['url'], data['resolution'])
        return jsonify({"url": url})
    except Exception as e:
        print(e.message)
        return "Internal Server Error"


@app.route('/playlist/download', methods=['POST'])
def playlist():
    data = request.json
    try:
        data = download_playlist(
            playlist_url=f'{data["url"]}', resolution=data['resolution'])
        return jsonify({"url": data})
    except Exception as e:
        print(e.message)
        return "Internal Server Error"


@app.errorhandler(404)
def not_found(error):
    return "<p>404 Route not found!</p>"


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)))
