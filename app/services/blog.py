from flask_sqlalchemy import SQLAlchemy
from flask_injector import inject
from app.models.blog import Blog
from app.models.like import Like
from app.models.dislike import Dislike
from sqlalchemy.orm import joinedload

class BlogService:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_all_posts(self):
        return Blog.query.options(joinedload(Blog.author), joinedload(Blog.likes), joinedload(Blog.dislikes)).all()

    def get_author_posts(self, author_id):
        return Blog.query.filter_by(author_id=author_id).all()

    def get_post(self, post_id):
        return Blog.query.get(post_id)

    def create_post(self, title, content, author_id):
        if not title or not content:
            return None, "Title and content are required."
        if len(title) < 5 :
            return None, "Title must be at least 5 characters long ."
        if len(content) < 20:
            return None, "Content must be at least 20 characters long."
        
        post = Blog(title=title, content=content, author_id=author_id)
        self.db.session.add(post)
        self.db.session.commit()
        return post, None

    def update_post(self, post_id, author_id=None, title=None, content=None, is_admin=False):
        post = self.get_post(post_id)

        # If it's an author, check that the author is the owner of the post
        if post and (is_admin or post.author_id == author_id): 
            if title and len(title) < 5:
                return None, "Title must be at least 5 characters long."
            if content and len(content) < 20:
                return None, "Content must be at least 20 characters long."
            if title:
                post.title = title
            if content:
                post.content = content

            self.db.session.commit()
            return post, None
        return None

    def delete_post(self, post_id, author_id):
        post = self.get_post(post_id)
        if post and post.author_id == author_id:
            self.db.session.delete(post)
            self.db.session.commit()
            return True
        return False

    def like_blog(self, blog_id, user_id):
        # Check if the user has already liked the blog
        existing_like = Like.query.filter_by(blog_id=blog_id, user_id=user_id).first()
        if existing_like:
            return None, "You have already liked this post."
        
        # Remove dislike if the user had previously disliked the blog
        existing_dislike = Dislike.query.filter_by(blog_id=blog_id, user_id=user_id).first()
        if existing_dislike:
            self.db.session.delete(existing_dislike)

        # Add the new like
        like = Like(blog_id=blog_id, user_id=user_id)
        self.db.session.add(like)
        self.db.session.commit()
        return like, None

    def dislike_blog(self, blog_id, user_id):
        # Check if the user has already disliked the blog
        existing_dislike = Dislike.query.filter_by(blog_id=blog_id, user_id=user_id).first()
        if existing_dislike:
            return None, "You have already disliked this post."
        
        # Remove like if the user had previously liked the blog
        existing_like = Like.query.filter_by(blog_id=blog_id, user_id=user_id).first()
        if existing_like:
            self.db.session.delete(existing_like)

        # Add the new dislike
        dislike = Dislike(blog_id=blog_id, user_id=user_id)
        self.db.session.add(dislike)
        self.db.session.commit()
        return dislike, None
