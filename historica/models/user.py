import bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from historica import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username is required")
        return username

    @staticmethod
    def hash_password(password: str) -> bytes:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def set_password(self, password: str):
        self.password_hash = User.hash_password(password)

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

    @classmethod
    def register(cls, username: str, password: str) -> 'User':
        user = cls(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def authenticate(cls, username: str, password: str) -> 'User':
        user = cls.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None
