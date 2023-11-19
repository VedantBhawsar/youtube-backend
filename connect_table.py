from pymongo import MongoClient


client = MongoClient(
    'mongodb+srv://admin:admin@cluster0.zqdyzpj.mongodb.net/?retryWrites=true&w=majority')

db = client["Youtube-Downloader"]
collection = db["Youtube-Downloader"]

videos = db.videos
playlists = db.playlists