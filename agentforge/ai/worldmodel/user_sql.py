# import bcrypt
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import validates
# from agentforge import db
# from flask import session

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True, nullable=False) #login name
#     password_hash = db.Column(db.String(128), nullable=False)
#     config = db.Column(db.JSON)  # Stores email, display name, etc.

#     @validates('username')
#     def validate_username(self, key, username):
#         if not username:
#             raise ValueError("Username is required")
#         return username

#     @staticmethod
#     def hash_password(password: str) -> bytes:
#         return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#     def set_password(self, password: str):
#         self.password_hash = User.hash_password(password)

#     def check_password(self, password: str) -> bool:
#         return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

#     @classmethod
#     def register(cls, username: str, password: str) -> 'User':
#         user = cls(username=username)
#         user.set_password(password)
#         db.session.add(user)
#         db.session.commit()
#         return user

#     @classmethod
#     def logout(cls, user_id: int):
#         session_key = f"user_{user_id}"
#         session.pop(session_key, None)

#     @classmethod
#     def authenticate(cls, username: str, password: str) -> 'User':
#         user = cls.query.filter_by(username=username).first()
#         if user and user.check_password(password):
#             session_key = f"user_{user.id}"
#             session[session_key] = user.id
#             return user
#         return None

#     def get_config(self) -> dict:
#         """Returns the configuration dictionary."""
#         return self.config or {}

#     def set_config(self, config_dict: dict):
#         """Updates the configuration dictionary with the provided dictionary."""
#         if self.config:
#             self.config.update(config_dict)
#         else:
#             self.config = config_dict
#         db.session.commit()
