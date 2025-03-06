from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'USERS'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    articles = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}')"

class Post(db.Model):
    __tablename__ = 'POSTS'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(75), nullable=False)
    body = db.Column(db.String(800), nullable=False)
    image_path = db.Column(db.String(100), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('USERS.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.timestamp}')"