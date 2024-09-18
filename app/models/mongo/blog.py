import datetime
from app import mongo


class Blog:
    def __init__(self, title, content, author_id):
        self.title = title
        self.content = content
        self.timestamp = datetime.datetime.utcnow()
        self.author_id = author_id
        self.likes = []
        self.dislikes = []

    def save(self):
        db = mongo.db
        db.blogs.insert_one({
            'title': self.title,
            'content': self.content,
            'timestamp': self.timestamp,
            'author_id': self.author_id,
            'likes': self.likes,
            'dislikes': self.dislikes
        })
