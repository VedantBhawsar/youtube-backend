from flask import Flask, request, jsonify
import cloudinary
from video_downloader import video_download

app = Flask(__name__)

cloudinary.config(
    cloud_name="dydrdxj16",
    api_key="415477486895499",
    api_secret="ME8tqQx09MiU5yHgMj1kWpq0MV0"
)


@app.route("/")
def main():
    return "<p>Api is working fine!</p>"


@app.route('/video/download', methods=['POST'])
def playlist():
    data = request.json
    print(data)
    try:
        data = video_download('https://youtu.be/DnazLKj71RQ', '360p')
        return jsonify({"result": data})
    except Exception as e:
        print(e.message)
        return "Internal Server Error"


@app.errorhandler(404)
def not_found(error):
    return "<p>404 Route not found!</p>"


if __name__ == '__main__':
    app.run(debug=True)
