from sqlalchemy import Column, String< Integer, Date, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Member(Base):
    __tablename__ = 'member'
    member_id = Column(Integer,primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)

class Author(Base):
    __tablename__ = 'author'
    author_id = Column(Integer,primary_key=True, autoincrement=True)
    name = Column(String)
    birth_date = Column(Date)

class Library(Base):
    __tablename__ = 'library'
    library_id = Column(Integer,primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)

class Book(Base):
    __tablename__ = 'Book'
    book_id = Column(Integer,primary_key=True, autoincrement=True)
    title = Column(String)
    isbn = Column(String, unique=True)
    published_date = Column(Date)
    author_id = Column(Integer,ForeignKey('author.author_id'))
    library_id = Column(Integer,ForeignKey('library.library_id'))
