from sqlalchemy import TIMESTAMP, Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func

class Note(db.Model):
    id = Column(Integer, primary_key=True)
    data = Column(String(10000))
    date = Column(TIMESTAMP(timezone=True), default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    firstname = Column(String(120))
    lastname = Column(String(120))
    email = Column(String(150), unique=True)
    password = Column(String(130))
    notes = relationship('Note', backref='user', lazy=True)
    profile = relationship('UserProfile', back_populates='user', uselist=False)

class UserProfile(db.Model):
    id = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    bio = Column(String(200))
    location = Column(String(100))
    workplace = Column(String(100))
    education = Column(String(100))
    highlights = Column(String(200))
    linkedin = Column(String(200))
    facebook = Column(String(200))
    instagram = Column(String(200))
    cover_photo = Column(String(200))
    media_upload = Column(String(200))
    media_type = Column(String(50))
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='profile')
    posts = relationship('tradepost', back_populates='author', lazy=True)

class tradepost(db.Model):
    __tablename__ = 'trade_posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=True)
    image = Column(String(100), nullable=True)
    category = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user_profile.id'), nullable=False)
    author = relationship('UserProfile', back_populates='posts')
    
    def __repr__(self):
        return f"<tradepost '{self.title}', posted by User ID {self.user_id}>"
