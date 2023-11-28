from pytube import YouTube, Playlist
import cloudinary
# from cloudinary import uploader
import shutil
from mega import Mega
import os


mega = Mega()
m = mega.login('vedantbhavsar.a10@gmail.com', 'password123@')
# cloudinary.config(
#     cloud_name="dydrdxj16",
#     api_key="415477486895499",
#     api_secret="ME8tqQx09MiU5yHgMj1kWpq0MV0"
# )


def video_download(url,  resolution, playlist,  index):
    try:
        yt = YouTube(url)
        path = yt.title.replace(' ', '_')
        playlist_name = playlist.title.replace(' ', '_')
        stream = yt.streams.filter(res=resolution).first()
        stream.download(
            output_path=f'/home/vedant/Videos/youtube/playlist/{playlist_name}', filename=f'{index}_{path}.mp4')
        print(f"Downloaded video: {yt.title}")
    except Exception as e:
        print(f'Something went wrong1: {str(e)}')


def download_playlist(playlist_url, resolution):
    try:
        playlist = Playlist(playlist_url)
        links = []
        playlist_name = playlist.title.replace(' ', '_')

        # file_exists = m.find(
        #     f'{playlist_name}_{resolution}.zip', exclude_deleted=True)
        # if file_exists is not None:
        #     url = m.get_link(file_exists)
        #     return url

        for index, url in enumerate(playlist):
            links.append(video_download(
                url, resolution, playlist, index=index+1))

        # shutil.make_archive(
        #     f'zipped/{playlist_name}_{resolution}', 'zip', f'videos/{playlist_name}')

        # file = m.upload(f'zipped/{playlist_name}_{resolution}.zip')
        # url = m.get_upload_link(file)
        # if os.path.exists(f"zipped/{playlist_name}_{resolution}.zip"):
        #     os.remove(f"zipped/{playlist_name}_{resolution}.zip")
        return url
    except Exception as e:
        print(f'Something went wrong: {e}')
