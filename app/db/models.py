from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from .session import Base

class TodoItem(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(Text)
    completed = Column(Boolean, default=False)

class User(Base):
    __tablename__ = "users"

    # id = Column(Integer, primary_key=True, index=True)
    # username = Column(String, unique=True, index=True)
    # email = Column(String, unique=True, index=True)
    # password = Column(String)
    # bio = Column(Text, nullable=True)
    # image = Column(String, nullable=True)

    # MySQL
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    bio = Column(Text, nullable=True)
    image = Column(String(255), nullable=True)

    articles = relationship("Article", back_populates="author")
    comments = relationship("Comment", back_populates="author")

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    title = Column(String(255))
    description = Column(Text)
    body = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="articles")
    comments = relationship("Comment", back_populates="article")
    tags = relationship("Tag", secondary="article_tags", back_populates="articles")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    body = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"))
    article_id = Column(Integer, ForeignKey("articles.id"))

    author = relationship("User", back_populates="comments")
    article = relationship("Article", back_populates="comments")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)

    articles = relationship("Article", secondary="article_tags", back_populates="tags")

article_tags = Table(
    'article_tags', Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
    )
