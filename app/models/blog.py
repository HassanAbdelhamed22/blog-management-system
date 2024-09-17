from flask_sqlalchemy import SQLAlchemy
from app import db


class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    likes = db.relationship('Like', backref='blog', lazy=True)
    dislikes = db.relationship('Dislike', backref='blog', lazy=True)
