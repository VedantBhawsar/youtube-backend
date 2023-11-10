import json
from flask import Flask, request, jsonify
import cloudinary
import get_info
from video_downloader import video_download
from playlist_downloader import download_playlist
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import JSON
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


class Video(db.Model):
    __tablename__ = 'videos'

    video_id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    thumbnail = db.Column(JSON, nullable=False)
    quality = db.Column(JSON, nullable=False)


class Playlist(db.Model):
    __tablename__ = 'playlists'

    playlist_id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    thumbnail = db.Column(JSON, nullable=True)
    quality = db.Column(JSON, nullable=False)


def __repr__(self):
    return f"Name : {self.first_name}, Age: {self.age}"


with app.app_context():
    db.create_all()


cloudinary.config(
    cloud_name="dydrdxj16",
    api_key="415477486895499",
    api_secret="ME8tqQx09MiU5yHgMj1kWpq0MV0"
)


@app.route("/")
def main():
    return "<p>Api is working fine!</p>"


@app.route('/video/get')
def get_video():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is missing"}, 400)
    video = get_info.get_video_info(url)
    video_data = {
        "video_id": video.video_id,
        "title": video.title,
        "thumbnail": json.loads(video.thumbnail),
        "quality": json.loads(video.quality)
    }
    return jsonify(video_data)


@app.route('/playlist/get')
def get_playlist():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is missing"}, 400)
    playlist = get_info.get_playlist_info(url)
    playlist_data = {
        "playlist_id": playlist.playlist_id,
        "title": playlist.title,
        "quality": json.loads(playlist.quality),
    }
    return jsonify(playlist_data)


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
    app.run(debug=True)
