from app import mongo


class Dislike:
    def __init__(self, user_id, blog_id):
        self.user_id = user_id
        self.blog_id = blog_id

    def save(self):
        db = mongo.db
        db.dislikes.insert_one({
            'user_id': self.user_id,
            'blog_id': self.blog_id
        })
