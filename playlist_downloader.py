import asyncio
import time
from pytube import YouTube, Playlist

playlist_url = input('Playlist URL: ')
resolution = input('Resolution: ')


import cloudinary
from cloudinary import uploader


cloudinary.config( 
  cloud_name = "dydrdxj16", 
  api_key = "415477486895499", 
  api_secret = "ME8tqQx09MiU5yHgMj1kWpq0MV0" 
)



async def measure_response_time(url, count, playlist):
    start_time = time.time()
    await video_download(url, count, playlist)
    end_time = time.time()
    response_time = end_time - start_time
    print(f"Response time for video {count}: {response_time:.2f} seconds")


async def video_download(url, count, playlist):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(res=resolution).first()
        print(f"Downloading video {count}: {yt.title}")
        await asyncio.to_thread(stream.download, filename_prefix=f"{count}_", output_path=f'videos/playlist/{playlist.title}')
        data = uploader.upload(f"./videos/playlist/{playlist.title}/{count}_{yt.title}.mp4", resource_type='video', public_id='video_upload_example')
        print(data['playback_url'])
        print(f"Downloaded video {count}: {yt.title}")
    except Exception as e:
        print(f'Something went wrong: {str(e)}')


async def print_elapsed_time():
    while True:
        print(f"Elapsed time: {time.time() - start_time:.2f} seconds")
        await asyncio.sleep(10)


async def download_playlist(playlist_url):
    playlist = Playlist(playlist_url)
    tasks = [measure_response_time(url, count, playlist) for count, url in enumerate(
        playlist.video_urls, start=1)]
    time_printer_task = asyncio.create_task(print_elapsed_time())
    await asyncio.gather(*tasks)
    time_printer_task.cancel()

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(download_playlist(playlist_url))