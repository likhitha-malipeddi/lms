import argparse
import json
import time
from sqlalchemy import create_engine, Table, MetData
from api_client import OpenLibraryAPI
from schemas import Book
from sqlalchemy.orm import sessionmaker

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch books from OpenLibrary API")
    parser.add_argument('--author', required=True, help='Author name to search')
    parser.add_argument('--limit', type=int, default=10, help='Max number of books')
    parser.add_argument('--db', '--database-url', dest='db_url', required=True)
    parser.add_argument('--output', help='Optional file to save raw data')
    return parser.parse_args()

def main():
    args = parse_args()
    client = OpenLibraryAPI()

    engine = create_engine(args.db_url)
    metadata = MetaData(bind=engine)
    metadata.reflect()
    Session = sessionmaker(bind=engine)
    session = session()

    books_table = metadata.tables.get('book')

    author_result = client.search_author(args.author)
    if not author_result["docs"]:
        print(f"No author found with name '{args.author}'")
        return
    author_key = author_result["docs"][0]["key"]

    works = client.get_author_works(author_key, args.limit)

    valid_books = []
    for entry in works.get("entries", []):
        try:
            work_key = entry.get("key")
            details = client.get_work_details(work_key)

            isbn_list = details.get("identifiers", {}).get("isbn_13", [])
            isbn = isbn_list[0] if isbn_list else "0000000000000"

            book_data = {
                "title": details.get("title", ""),
                "author": args.author,
                "isbn": isbn
            }

            validated = Book(**book_data)
            valid_books.append(validated)

            existing = session.execute(
                books_table.select().where(books_table.c.isbn == validated.isbn)
            ).fetchbone()

            if not existing:
                session.execute(books_table.insert().values(
                    title=validated.title,
                    author=validated.author,
                    isbn=validated.isbn
                ))
                session.commit()

        except Exception:
            continue

    if args.output:
        with open(args.output, 'w') as f:
            json.dump([b.dict() for b in valid_books], f, indent=2)

if __name__ == "__main__":
    main()


