from sqlalchemy import func
from sqlalchemy.orm import Session
from models import Book, Author
from database import SessionLocal


def create_book(session: Session, title: str, genre: str, authors: list[str]):
    book = Book(title=title, genre=genre)
    for author in authors:
        author_obj = session.query(Author).filter_by(name=author).first()
        if not author_obj:
            author_obj = Author(name=author)
            session.add(author_obj)
        book.authors.append(author_obj)
    session.add(book)
    session.commit()


# ===== TASK VI. Joins are used here =====
def get_all_books():
    session = SessionLocal()
    query = (
        session.query(Book)
        .join(Book.authors)
    )
    return query.all()


def get_books_by_title(title):
    session = SessionLocal()
    query = (
        session.query(Book)
        .filter_by(title=title)
        .join(Book.authors)
    )
    return query.all()


def get_books_by_genre(genre):
    session = SessionLocal()
    query = (
        session.query(Book)
        .filter_by(genre=genre)
        .join(Book.authors)
    )
    return query.all()


def search_books_by_author(session: Session, author_name: str):
    # First, filter authors by name (case-insensitive)
    author_query = (
        session.query(Author.id)
        .filter(func.lower(Author.name) == func.lower(author_name))
    )

    book_query = (
        session.query(Book)
        .join(Author, Book.authors)
        .filter(Author.id.in_(author_query.subquery().select()))  # Explicitly call select()
    )

    return book_query.all()
