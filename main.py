from database import SessionLocal
from crud.books import create_book, get_all_books, get_books_by_title, get_books_by_genre, search_books_by_author
from crud.authors import create_author
from sqlalchemy import select, func
from database import engine
from models import Base, Book, Author

# Base.metadata.create_all(engine)

# Usage of the project's code
with SessionLocal() as session:
    # # add an author with no books
    # create_author(session, name="Darmen Tuyaq")
    #
    # # add several books
    # create_book(session, title="The Lord of the Rings", genre="Fantasy", authors=["J.R.R. Tolkien"])
    # create_book(session, title="The Hobbit", genre="Fantasy", authors=["J.R.R. Tolkien"])
    # create_book(session, title="A Game of Thrones", genre="Fantasy", authors=["George R. R. Martin"])
    # create_book(session, title="1984", genre="Dystopian", authors=["George Orwell"])
    # create_book(session, title="Programming Python", genre="Computer Science", authors=["Mark Lutz"])
    #
    # # one book by several authors
    # create_book(session, title="C Programming Language",
    #             genre="Computer Science",
    #             authors=["Brian W. Kernighan", "Dennis M. Ritchie"]
    #             )

    # ===== TASK I. SUBQUERY. Used to show top 3 genres by quantity  =====
    print("=== TASK I. Subquery. Show top 3 genres by quantity ===")
    subquery = (
        select(Book.genre, func.count(Book.id).label("book_count"))
        .group_by(Book.genre)
        .order_by(func.count(Book.id).desc())
        .limit(3)
    ).subquery()

    query = (
        select(subquery.c.genre, subquery.c.book_count)
    )
    results = session.execute(query).all()

    for row in results:
        print(f"Genre: {row.genre}, Book Count: {row.book_count}")

    # ===== TASK III. Aggregate function used here =====
    # Retrieves all books and counts the total number of books
    print("\n=== TASK III. Aggregate function. Retrieve all books and count the total number of books ===")
    books = get_all_books()
    total_book_count = session.query(func.count(Book.id)).scalar()  # Aggregate function

    print("Total number of books:", total_book_count)

    # Print information about each book
    for book in books:
        print(f"Title: {book.title}, Genre: {book.genre}")
        for author in book.authors:
            print(f"- Author: {author.name}")

    # COMMAND LINE INTERFACE
    print("\nCOMMAND LINE INTERFACE")
    while True:
        print("Welcome to library\n"
              "1. List all books\n"
              "2. Search by title\n"
              "3. Search by genre\n"
              "4. Search by author")
        try:
            option = int(input("Choose an option: "))

            if option == 1:
                print("You've chosen to list all books in the library:")
                books = get_all_books()

                # Print information about each book
                for book in books:
                    print(f"Title: {book.title}, Genre: {book.genre}")
                    for author in book.authors:
                        print(f"- Author: {author.name}")
                continue

            if option == 2:
                query = input("Enter title to search: ")
                books = get_books_by_title(query)

                for book in books:
                    print(f"Title: {book.title}, Genre: {book.genre}")
                    for author in book.authors:
                        print(f"- Author: {author.name}")

                if len(books) == 0:
                    print(f"There is no books in our database that have '{query}' in their title")
                continue

            if option == 3:
                query = input("Enter genre to search: ")
                books = get_books_by_genre(query)

                for book in books:
                    print(f"Title: {book.title}, Genre: {book.genre}")
                    for author in book.authors:
                        print(f"- Author: {author.name}")

                if len(books) == 0:
                    print(f"There is no books in our database of '{query}' genre")
                continue

            if option == 4:
                # Get author name from user input or other source
                author_name = input("Enter author name to search for: ")

                # Call the search function with the author name
                searched_books = search_books_by_author(session, author_name)

                if searched_books:
                    print(f"Found books by author '{author_name}':")
                    for book in searched_books:
                        print(f"\tTitle: {book.title}, Genre: {book.genre}")
                else:
                    print(f"No books found by author '{author_name}'.")
                continue

            else:
                print("Please enter correct number")
                continue
        except ValueError:
            print("Please enter correct number")
            continue


