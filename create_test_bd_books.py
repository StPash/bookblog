from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine('sqlite:///db_books_log.db')
Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id_book = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id_author"))
    author = relationship('Author')
    genres = relationship('BookGenre')
    description = Column(Text)
    image_url = Column(String)


class User(Base):
    __tablename__ = 'users'

    id_user = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)


class FinishedBook(Base):
    __tablename__ = 'finished_books'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id_user"))
    book_id = Column(Integer, ForeignKey("books.id_book"))


class DesiredBook(Base):
    __tablename__ = 'desired_books'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id_user"))
    book_id = Column(Integer, ForeignKey("books.id_book"))


class Author(Base):
    __tablename__ = 'authors'

    id_author = Column(Integer, primary_key=True)
    surname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    patronymic = Column(String)


class Genre(Base):
    __tablename__ = 'genres'

    id_genre = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class BookGenre(Base):
    __tablename__ = 'books_and_genres'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id_book"))
    genre_id = Column(Integer, ForeignKey("genres.id_genre"))


Base.metadata.create_all(bind=engine)
