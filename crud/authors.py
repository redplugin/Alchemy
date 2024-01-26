from sqlalchemy.orm import Session
from models import Author
from database import SessionLocal


def create_author(session: Session, name: str):
    author = Author(name=name)
    session.add(author)
    session.commit()
