from pytube import YouTube
# from mega import Mega
import os


# mega = Mega()
# m = mega.login('vedantbhavsar.a10@gmail.com', 'password123@')


def video_download(url,  resolution):
    try:
        yt = YouTube(url)
        path = yt.title.replace(' ', '_')
        stream = yt.streams.filter(res=resolution).first()

        # file_exists = m.find(
        #     f'{path}_{resolution}.mp4', exclude_deleted=True)
        # if file_exists is not None:
        #     print(file_exists)
        #     url = m.get_link(file_exists)
        #     return url

        stream.download(output_path=f'/home/vedant/Videos/youtube/videos',
                        filename=f'{path}_{resolution}.mp4')
        print(f"Downloaded video: {yt.title}")

        # Here you can Upload to your mega drive
        # folder = m.find('videos')
        # file = m.upload(f'videos/{path}_{resolution}.mp4', folder[0])
        # url = m.get_upload_link(file)
        return url
    except Exception as e:
        print(f'Something went wrong: {str(e)}')
