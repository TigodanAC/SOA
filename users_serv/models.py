from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.String(36), primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    profile = db.relationship('UserProfile', backref='users', uselist=False, cascade='all, delete-orphan')


class UserProfile(db.Model):
    __tablename__ = 'profiles'
    profile_id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    avatar = db.Column(db.String(200))
    description = db.Column(db.Text)
    date_of_birth = db.Column(db.DateTime)


class UserSubscriptions(db.Model):
    __tablename__ = 'subscriptions'
    sub_id = db.Column(db.String(36), primary_key=True)
    follower_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    followee_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    is_mutual = db.Column(db.Boolean, default=False)
    sub_time = db.Column(db.DateTime, default=datetime.utcnow)
