import json
from pytube import YouTube, Playlist
import re
# from main import Video
import main


def is_video_info_available_in_db(yt):
    video = main.Video.query.filter_by(video_id=yt.video_id).first()
    if video:
        return video
    else:
        return 'None'


def get_video_info(url):
    quality = []
    yt = YouTube(url)
    video = is_video_info_available_in_db(yt)
    if (video != 'None'):
        return video

    for x in (yt.streams.filter(progressive=True)):
        res_match = re.search(r'res="([^"]+)"', str(x))
        quality.append(str(res_match.group(1)))
        yt.vid_info['videoDetails']

    video_id = yt.vid_info['videoDetails']['videoId']
    title = yt.vid_info['videoDetails']['title']
    thumbnail = yt.vid_info['videoDetails']['thumbnail']['thumbnails']
    thumbnail_json = json.dumps(
        thumbnail[len(thumbnail)-1]
    )
    quality = json.dumps(quality)

    video_data = main.Video(video_id=video_id, title=title,
                            thumbnail=thumbnail_json, quality=quality)
    main.db.session.add(video_data)
    main.db.session.commit()
    return video_data


def is_playlist_info_available_in_db(playlist):
    video = main.Playlist.query.filter_by(
        playlist_id=playlist.playlist_id).first()
    if video:
        return video
    else:
        return 'None'


def get_playlist_info(url):
    quality = ['144p', '240p', '360p', '720p', '1080p']
    pl = Playlist(url)
    playlist = is_playlist_info_available_in_db(pl)
    if (playlist != 'None'):
        return playlist

    playlist_id = pl.playlist_id
    title = pl.title
    quality = json.dumps(quality)

    playlist_data = main.Playlist(
        playlist_id=playlist_id, title=title, quality=quality)
    main.db.session.add(playlist_data)
    main.db.session.commit()
    return playlist_data
