from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# ===== TASK IV. Foreign Keys are used here  =====
# ===== TASK V. Many-to-Many tables are implemented here  =====
book_authors_association = Table(
    "book_authors_association",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id")),
    Column("author_id", Integer, ForeignKey("authors.id")),
)


# ===== TASK II. CONSTRAINTS are used here  =====
class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

    books = relationship("Book", secondary="book_authors_association", back_populates="authors")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    genre = Column(String(128))

    authors = relationship("Author", secondary="book_authors_association", back_populates="books")



