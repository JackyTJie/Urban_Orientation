from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Global variable to hold the db instance
_db = None

def init_db(database):
    global _db
    _db = database
    # Now that _db is set, we can define the models
    global User, Admin, Activity, Keyword, Content, Conversation
    User = _create_user_model()
    Admin = _create_admin_model()
    Activity = _create_activity_model()
    Keyword = _create_keyword_model()
    Content = _create_content_model()
    Conversation = _create_conversation_model()

def _create_user_model():
    class User(_db.Model):
        __tablename__ = 'users'

        id = _db.Column(_db.Integer, primary_key=True)
        username = _db.Column(_db.String(80), unique=True, nullable=False)
        email = _db.Column(_db.String(120), unique=True, nullable=False)
        password_hash = _db.Column(_db.String(120), nullable=False)
        created_at = _db.Column(_db.DateTime, default=datetime.utcnow)

        # Relationship with conversations
        conversations = _db.relationship('Conversation', backref='user', lazy=True)

        def __repr__(self):
            return f'<User {self.username}>'
    return User

def _create_admin_model():
    class Admin(_db.Model):
        __tablename__ = 'admins'

        id = _db.Column(_db.Integer, primary_key=True)
        username = _db.Column(_db.String(80), unique=True, nullable=False)
        password_hash = _db.Column(_db.String(120), nullable=False)
        role = _db.Column(_db.String(20), default='regular')  # 'root' or 'regular'
        created_at = _db.Column(_db.DateTime, default=datetime.utcnow)

        def __repr__(self):
            return f'<Admin {self.username}>'
    return Admin

def _create_activity_model():
    class Activity(_db.Model):
        __tablename__ = 'activities'

        id = _db.Column(_db.Integer, primary_key=True)
        title = _db.Column(_db.String(200), nullable=False)
        description = _db.Column(_db.Text)
        bot_name = _db.Column(_db.String(100), default='Activity Bot')
        created_at = _db.Column(_db.DateTime, default=datetime.utcnow)
        updated_at = _db.Column(_db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

        # Relationship with keywords
        keywords = _db.relationship('Keyword', backref='activity', lazy=True, cascade='all, delete-orphan')

        def __repr__(self):
            return f'<Activity {self.title}>'
    return Activity

def _create_keyword_model():
    class Keyword(_db.Model):
        __tablename__ = 'keywords'

        id = _db.Column(_db.Integer, primary_key=True)
        activity_id = _db.Column(_db.Integer, _db.ForeignKey('activities.id'), nullable=False)
        keyword = _db.Column(_db.String(100), nullable=False)
        created_at = _db.Column(_db.DateTime, default=datetime.utcnow)

        # Relationship with content
        content = _db.relationship('Content', backref='keyword', lazy=True, cascade='all, delete-orphan')
        # Relationship with conversations
        conversations = _db.relationship('Conversation', backref='keyword', lazy=True)

        def __repr__(self):
            return f'<Keyword {self.keyword}>'
    return Keyword

def _create_content_model():
    class Content(_db.Model):
        __tablename__ = 'content'

        id = _db.Column(_db.Integer, primary_key=True)
        keyword_id = _db.Column(_db.Integer, _db.ForeignKey('keywords.id'), nullable=False)
        content_type = _db.Column(_db.String(10), default='text')  # 'text' or 'photo'
        content_text = _db.Column(_db.Text)
        content_photo_path = _db.Column(_db.String(200))  # Path to stored photo
        created_at = _db.Column(_db.DateTime, default=datetime.utcnow)

        def __repr__(self):
            return f'<Content {self.content_type} for keyword {self.keyword.keyword}>'
    return Content

def _create_conversation_model():
    class Conversation(_db.Model):
        __tablename__ = 'conversations'

        id = _db.Column(_db.Integer, primary_key=True)
        user_id = _db.Column(_db.Integer, _db.ForeignKey('users.id'), nullable=False)
        activity_id = _db.Column(_db.Integer, _db.ForeignKey('activities.id'), nullable=False)
        keyword_id = _db.Column(_db.Integer, _db.ForeignKey('keywords.id'), nullable=False)
        message = _db.Column(_db.Text, nullable=False)
        timestamp = _db.Column(_db.DateTime, default=datetime.utcnow)
        sender_type = _db.Column(_db.String(10), default='user')  # 'user' or 'bot'

        def __repr__(self):
            return f'<Conversation by {self.user.username} at {self.timestamp}>'

        def is_bot_message(self):
            """Check if this is a bot message"""
            return self.sender_type == 'bot'
    return Conversation