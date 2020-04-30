import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("URL"))
db = scoped_session(sessionmaker(bind=engine))


def create_table():
    db.execute("CREATE TABLE books(isbn VARCHAR NOT NULL, title VARCHAR NOT NULL, author VARCHAR NOT NULL, year INTEGER NOT NULL);")
    print("Table created")
    db.commit()


def import_books():
    books = csv.reader(open("books.csv"))
    for isbn, title, author, year in books:
        if isbn != "isbn":
            db.execute("INSERT INTO books(isbn, title, author, year) VALUES (:i, :t, :a, :y);", {"i": isbn, "t": title, "a": author, "y": year})
            print(f"Adding book with values(isbn: {isbn}, title: {title}, author: {author}, year: {year})")
    db.commit()


def main():
    create_table()
    import_books()


if __name__ == "__main__":
    main()
