import json
from pytube import YouTube, Playlist
import re
from connect_table import videos, playlists
import main
from bs4 import BeautifulSoup
import requests


def is_video_info_available_in_db(yt):
    video = main.Video.query.filter_by(video_id=yt.video_id).first()
    if video:
        return video
    else:
        return 'None'


def get_video_info(url):
    quality = []
    yt = YouTube(url)
    video = videos.find_one({"_id": str(yt.video_id)})
    if video:
        return video

    for x in (yt.streams.filter(progressive=True)):
        res_match = re.search(r'res="([^"]+)"', str(x))
        quality.append(str(res_match.group(1)))
        yt.vid_info['videoDetails']

    video_id = yt.vid_info['videoDetails']['videoId']
    title = yt.vid_info['videoDetails']['title']
    thumbnail = yt.vid_info['videoDetails']['thumbnail']['thumbnails']
    video_data = {
        "_id":str(video_id),
        "title": str(title),
        "thumbnail": thumbnail[len(thumbnail)-1],
        "quality": quality,
    }
    id = videos.insert_one(video_data).inserted_id
    video = videos.find_one({"_id": id})
    return video

def get_playlist_info(url):
    quality = ['144p', '240p', '360p', '720p', '1080p']
    pl = Playlist(url)
    
    playlist = playlists.find_one({"_id": pl.playlist_id})
    if playlist:
        return playlist
    
    playlist_renderer = pl.initial_data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"][
        "sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]["playlistVideoListRenderer"]["contents"]
    thumbnails = []
    for video in playlist_renderer:
        thumbnail_url = video["playlistVideoRenderer"]["thumbnail"]["thumbnails"][-1]["url"]
        thumbnails.append(thumbnail_url)
    id = pl.playlist_id
    title = pl.title
    
    playlist_data = {
        "_id": str(id),
        "title": str(title),
        "thumbnail": {"url":thumbnails[len(thumbnails)-1]},
        "quality": quality,
    }
    id = playlists.insert_one(playlist_data).inserted_id
    playlist = playlists.find_one({"_id": id})
    return playlist
