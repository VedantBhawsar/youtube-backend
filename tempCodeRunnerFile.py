video_id = db.Column(db.String, primary_key=True, unique=True)
    title = db.Column(db.String(50), nullable=False)
    thumbnail = db.Column(JSON, nullable=False)
    quality = db.Column(JSON, nullable=False)