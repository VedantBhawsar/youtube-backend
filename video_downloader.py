from pytube import YouTube
import cloudinary
from cloudinary import uploader


cloudinary.config(
    cloud_name="dydrdxj16",
    api_key="415477486895499",
    api_secret="ME8tqQx09MiU5yHgMj1kWpq0MV0"
)


def video_download(url,  resolution):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(res=resolution).first()
        print(f"Downloading video:- {yt.title}")
        stream.download(output_path=f'videos')
        data = uploader.upload(
            f"./videos/{yt.title}.mp4", resource_type='video', public_id='video_upload_example')
        print(f"Downloaded video: {yt.title}")
        return data['url']
    except Exception as e:
        print(f'Something went wrong: {str(e)}')
