from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base 


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)  # ✅ New field
    role = Column(String(50), default='User')
    password = Column(String(200), nullable=False)  # ✅ Increased length for hashed password

    # Relationship to posts
    posts = relationship("Post", back_populates="owner")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship back to user
    owner = relationship("User", back_populates="posts")
