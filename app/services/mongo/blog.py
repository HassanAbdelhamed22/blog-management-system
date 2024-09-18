from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import datetime

class BlogService:
    def __init__(self, mongo: PyMongo):
        self.mongo = mongo

    def get_all_posts(self):
        return list(self.mongo.db.blogs.find())

    def get_author_posts(self, author_id):
        return list(self.mongo.db.blogs.find({'author_id': ObjectId(author_id)}))

    def get_post(self, post_id):
        return self.mongo.db.blogs.find_one({'_id': ObjectId(post_id)})

    def create_post(self, title, content, author_id):
        if not title or not content:
            return None, "Title and content are required."
        if len(title) < 5:
            return None, "Title must be at least 5 characters long."
        if len(content) < 20:
            return None, "Content must be at least 20 characters long."
        
        post = {
            'title': title,
            'content': content,
            'author_id': ObjectId(author_id),
            'timestamp': datetime.datetime.utcnow()
        }
        result = self.mongo.db.blogs.insert_one(post)
        return self.mongo.db.blogs.find_one({'_id': result.inserted_id}), None

    def update_post(self, post_id, author_id=None, title=None, content=None, is_admin=False):
        post = self.get_post(post_id)

        if post and (is_admin or post['author_id'] == ObjectId(author_id)):
            if title and len(title) < 5:
                return None, "Title must be at least 5 characters long."
            if content and len(content) < 20:
                return None, "Content must be at least 20 characters long."
            update_data = {}
            if title:
                update_data['title'] = title
            if content:
                update_data['content'] = content

            self.mongo.db.blogs.update_one({'_id': ObjectId(post_id)}, {'$set': update_data})
            return self.get_post(post_id), None
        return None

    def delete_post(self, post_id, author_id=None, is_admin=False):
        post = self.get_post(post_id)
        if post and (is_admin or post['author_id'] == ObjectId(author_id)):
            self.mongo.db.likes.delete_many({'blog_id': ObjectId(post_id)})
            self.mongo.db.dislikes.delete_many({'blog_id': ObjectId(post_id)})
            self.mongo.db.blogs.delete_one({'_id': ObjectId(post_id)})
            return True
        return False

    def like_blog(self, blog_id, user_id):
        if self.mongo.db.likes.find_one({'blog_id': ObjectId(blog_id), 'user_id': ObjectId(user_id)}):
            return None, "You have already liked this post."

        if self.mongo.db.dislikes.find_one({'blog_id': ObjectId(blog_id), 'user_id': ObjectId(user_id)}):
            self.mongo.db.dislikes.delete_one({'blog_id': ObjectId(blog_id), 'user_id': ObjectId(user_id)})

        like = {
            'blog_id': ObjectId(blog_id),
            'user_id': ObjectId(user_id)
        }
        self.mongo.db.likes.insert_one(like)
        return like, None

    def dislike_blog(self, blog_id, user_id):
        if self.mongo.db.dislikes.find_one({'blog_id': ObjectId(blog_id), 'user_id': ObjectId(user_id)}):
            return None, "You have already disliked this post."

        if self.mongo.db.likes.find_one({'blog_id': ObjectId(blog_id), 'user_id': ObjectId(user_id)}):
            self.mongo.db.likes.delete_one({'blog_id': ObjectId(blog_id), 'user_id': ObjectId(user_id)})

        dislike = {
            'blog_id': ObjectId(blog_id),
            'user_id': ObjectId(user_id)
        }
        self.mongo.db.dislikes.insert_one(dislike)
        return dislike, None
