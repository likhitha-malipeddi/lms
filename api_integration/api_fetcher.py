import argparse
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api_client import OpenLibraryClient
from Data_Ingestion.schemas import Book
from Data_Ingestion.models import Book as BookModel, Base

def map_api_book_to_db(api_data):
    try:
        return Book(
            title=api_data.get("title"),
            description=api_data.get("description", ""),
            isbn=api_data.get("isbn_13", [""])[0] if api_data.get("isbn_13") else None
        )
    except Exception as e:
        print(f"Validation failed: {e}")
        return None

def save_to_database(session, book: Book):
    exists = session.query(BookModel).filter_by(title=book.title).first()
    if not exists:
        book_model = BookModel(
            title=book.title,
            description=book.description,
            isbn=book.isbn
        )
        session.add(book_model)
        session.commit()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--author", required=True)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--db", "--database-url", required=True)
    parser.add_argument("--output", help="Optional JSON output file")
    args = parser.parse_args()

    engine = create_engine(args.db)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)

    client = OpenLibraryClient()

    author_search = client.search_author(args.author)
    if not author_search or not author_search["docs"]:
        print("Author not found.")
        return

    author_key = author_search["docs"][0]["key"]
    works = client.get_author_works(author_key, args.limit)

    raw_data = []
    for work in works.get("entries", []):
        work_key = work["key"]
        book_data = client.get_book_details(work_key)
        if book_data:
            raw_data.append(book_data)
            book = map_api_book_to_db(book_data)
            if book:
                save_to_database(session, book)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(raw_data, f, indent=2)

if __name__ == "__main__":
    main()